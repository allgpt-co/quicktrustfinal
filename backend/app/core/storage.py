"""S3-compatible object-storage helper with graceful degradation.

Production uses Amazon S3. Local development can point ``S3_ENDPOINT_URL`` at
MinIO, LocalStack, or another S3-compatible endpoint while exercising the same
boto3 code path used in production.
"""

from __future__ import annotations

import hashlib
import io
import logging
from datetime import timedelta
from typing import Any, Iterator

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.config import get_settings

logger = logging.getLogger(__name__)

_client: Any | None = None
_available: bool = False
_ensured_buckets: set[str] = set()


class StorageResponse:
    """Small compatibility wrapper for streamed object downloads.

    Existing API call sites expect the MinIO response methods ``read``,
    ``stream``, ``close``, and ``release_conn``. This wrapper keeps that local
    contract stable while the storage backend uses boto3.
    """

    def __init__(self, body: Any, content_type: str | None = None):
        self._body = body
        self.headers = {
            "content-type": content_type or "application/octet-stream",
        }

    def read(self, amount: int = -1) -> bytes:
        return self._body.read(amount)

    def stream(self, chunk_size: int = 32 * 1024) -> Iterator[bytes]:
        while True:
            chunk = self._body.read(chunk_size)
            if not chunk:
                break
            yield chunk

    def close(self) -> None:
        close = getattr(self._body, "close", None)
        if close:
            close()

    def release_conn(self) -> None:
        release_conn = getattr(self._body, "release_conn", None)
        if release_conn:
            release_conn()


def _get_client() -> Any | None:
    """Lazily initialise the global S3 client."""
    global _client, _available

    if _client is not None:
        return _client if _available else None

    settings = get_settings()
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY:
        logger.warning("S3 credentials are not configured. File storage will be disabled.")
        _available = False
        return None

    addressing_style = "path" if settings.S3_FORCE_PATH_STYLE else "auto"
    client_kwargs: dict[str, Any] = {
        "service_name": "s3",
        "region_name": settings.AWS_REGION,
        "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
        "config": Config(s3={"addressing_style": addressing_style}),
    }
    if settings.AWS_SESSION_TOKEN:
        client_kwargs["aws_session_token"] = settings.AWS_SESSION_TOKEN
    if settings.S3_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = settings.S3_ENDPOINT_URL

    try:
        _client = boto3.client(**client_kwargs)
        _available = True
        logger.info(
            "S3 object storage client initialized for region %s%s",
            settings.AWS_REGION,
            f" at {settings.S3_ENDPOINT_URL}" if settings.S3_ENDPOINT_URL else "",
        )
    except Exception as exc:
        logger.warning("S3 client initialization failed (%s). File storage will be disabled.", exc)
        _available = False

    return _client if _available else None


def _error_code(exc: ClientError) -> str:
    return str(exc.response.get("Error", {}).get("Code", ""))


def _is_sse_unsupported_error(exc: ClientError) -> bool:
    code = _error_code(exc)
    message = str(exc)
    lower_message = message.lower()
    return (
        code in {"NotImplemented", "NotSupported"}
        or "kms not configured" in lower_message
        or ("server side encryption" in lower_message and "not" in lower_message)
    )


def _create_bucket(client: Any, bucket: str) -> None:
    settings = get_settings()
    kwargs: dict[str, Any] = {"Bucket": bucket}
    if settings.AWS_REGION and settings.AWS_REGION != "us-east-1":
        kwargs["CreateBucketConfiguration"] = {"LocationConstraint": settings.AWS_REGION}
    client.create_bucket(**kwargs)
    logger.info("Created S3 bucket: %s", bucket)


def _ensure_bucket(client: Any, bucket: str) -> None:
    """Validate or create the bucket if configured to do so."""
    if bucket in _ensured_buckets:
        return

    settings = get_settings()
    try:
        client.head_bucket(Bucket=bucket)
    except ClientError as exc:
        if _error_code(exc) in {"404", "NoSuchBucket", "NotFound"} and settings.S3_CREATE_BUCKET:
            _create_bucket(client, bucket)
        else:
            logger.error("Failed to access S3 bucket '%s': %s", bucket, exc)
            raise

    _ensured_buckets.add(bucket)


def _read_bytes(data: bytes | io.BytesIO | Any) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, io.BytesIO):
        return data.getvalue()
    if hasattr(data, "read"):
        return data.read()
    return bytes(data)


def upload_file(
    bucket: str,
    object_name: str,
    data: bytes | io.BytesIO,
    content_type: str = "application/octet-stream",
) -> str:
    """Upload *data* and return the object path ``bucket/object_name``.

    Returns an empty string when object storage is unavailable.
    """
    client = _get_client()
    if client is None:
        logger.warning("S3 unavailable - skipping upload of %s/%s", bucket, object_name)
        return ""

    try:
        _ensure_bucket(client, bucket)
        raw = _read_bytes(data)
        sha256_hash = hashlib.sha256(raw).hexdigest()

        put_kwargs: dict[str, Any] = {
            "Bucket": bucket,
            "Key": object_name,
            "Body": raw,
            "ContentType": content_type,
            "Metadata": {"sha256": sha256_hash},
        }
        settings = get_settings()
        if settings.S3_SERVER_SIDE_ENCRYPTION:
            put_kwargs["ServerSideEncryption"] = settings.S3_SERVER_SIDE_ENCRYPTION

        try:
            client.put_object(**put_kwargs)
        except ClientError as exc:
            if "ServerSideEncryption" in put_kwargs and _is_sse_unsupported_error(exc):
                fallback_kwargs = dict(put_kwargs)
                fallback_kwargs.pop("ServerSideEncryption", None)
                client.put_object(**fallback_kwargs)
                logger.info(
                    "Uploaded %s/%s without SSE because the endpoint does not support it",
                    bucket,
                    object_name,
                )
            else:
                raise

        logger.info(
            "Uploaded %s/%s (%s, sha256=%s)",
            bucket,
            object_name,
            content_type,
            sha256_hash[:16],
        )
        return f"{bucket}/{object_name}"
    except (BotoCoreError, ClientError) as exc:
        logger.error("Upload failed for %s/%s: %s", bucket, object_name, exc)
        raise


def get_presigned_url(
    bucket: str,
    object_name: str,
    expires: timedelta | None = None,
) -> str:
    """Return a presigned GET URL valid for *expires* (default 1 hour).

    Returns an empty string when object storage is unavailable.
    """
    client = _get_client()
    if client is None:
        logger.warning(
            "S3 unavailable - cannot generate presigned URL for %s/%s",
            bucket,
            object_name,
        )
        return ""

    if expires is None:
        expires = timedelta(hours=1)

    try:
        return client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_name},
            ExpiresIn=int(expires.total_seconds()),
        )
    except (BotoCoreError, ClientError) as exc:
        logger.error(
            "Presigned URL generation failed for %s/%s: %s", bucket, object_name, exc
        )
        raise


def download_file(bucket: str, object_name: str) -> StorageResponse | None:
    """Return a response object for streaming.

    Returns ``None`` when object storage is unavailable.
    """
    client = _get_client()
    if client is None:
        logger.warning("S3 unavailable - cannot download %s/%s", bucket, object_name)
        return None

    try:
        response = client.get_object(Bucket=bucket, Key=object_name)
        return StorageResponse(
            body=response["Body"],
            content_type=response.get("ContentType"),
        )
    except (BotoCoreError, ClientError) as exc:
        logger.error("Download failed for %s/%s: %s", bucket, object_name, exc)
        raise


def delete_file(bucket: str, object_name: str) -> None:
    """Delete an object. No-op when object storage is unavailable."""
    client = _get_client()
    if client is None:
        logger.warning("S3 unavailable - skipping delete of %s/%s", bucket, object_name)
        return

    try:
        client.delete_object(Bucket=bucket, Key=object_name)
        logger.info("Deleted %s/%s", bucket, object_name)
    except (BotoCoreError, ClientError) as exc:
        logger.error("Delete failed for %s/%s: %s", bucket, object_name, exc)
        raise


def check_storage() -> tuple[bool, str | None]:
    """Probe configured object-storage buckets for readiness checks."""
    client = _get_client()
    if client is None:
        return False, "client not initialized"

    settings = get_settings()
    buckets = [settings.S3_BUCKET, settings.S3_REPORTS_BUCKET]
    try:
        for bucket in dict.fromkeys(bucket for bucket in buckets if bucket):
            _ensure_bucket(client, bucket)
        return True, None
    except (BotoCoreError, ClientError) as exc:
        return False, str(exc)[:200]
