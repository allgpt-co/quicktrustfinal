from __future__ import annotations

import io

import pytest
from botocore.exceptions import ClientError


class FakeBody:
    def __init__(self, data: bytes):
        self._buffer = io.BytesIO(data)
        self.closed = False

    def read(self, amount: int = -1) -> bytes:
        return self._buffer.read(amount)

    def close(self) -> None:
        self.closed = True


class FakeS3Client:
    def __init__(self, *, missing_bucket: bool = False, reject_sse: bool = False):
        self.missing_bucket = missing_bucket
        self.reject_sse = reject_sse
        self.head_bucket_calls = []
        self.create_bucket_calls = []
        self.put_object_calls = []
        self.delete_object_calls = []
        self.presigned_calls = []

    def head_bucket(self, *, Bucket: str) -> dict:
        self.head_bucket_calls.append(Bucket)
        if self.missing_bucket:
            raise ClientError(
                {"Error": {"Code": "404", "Message": "Not Found"}},
                "HeadBucket",
            )
        return {}

    def create_bucket(self, **kwargs) -> dict:
        self.create_bucket_calls.append(kwargs)
        return {}

    def put_object(self, **kwargs) -> dict:
        self.put_object_calls.append(kwargs)
        if self.reject_sse and "ServerSideEncryption" in kwargs:
            raise ClientError(
                {"Error": {"Code": "NotImplemented", "Message": "KMS not configured"}},
                "PutObject",
            )
        return {}

    def generate_presigned_url(self, ClientMethod: str, Params: dict, ExpiresIn: int) -> str:
        self.presigned_calls.append((ClientMethod, Params, ExpiresIn))
        return f"https://signed.example/{Params['Bucket']}/{Params['Key']}"

    def get_object(self, **kwargs) -> dict:
        return {
            "Body": FakeBody(b"stored-data"),
            "ContentType": "text/plain",
            "Metadata": {"sha256": "abc123"},
        }

    def delete_object(self, **kwargs) -> dict:
        self.delete_object_calls.append(kwargs)
        return {}


class FakeSettings:
    AWS_ACCESS_KEY_ID = "access-key"
    AWS_SECRET_ACCESS_KEY = "secret-key"
    AWS_SESSION_TOKEN = ""
    AWS_REGION = "us-west-2"
    S3_ENDPOINT_URL = ""
    S3_FORCE_PATH_STYLE = False
    S3_CREATE_BUCKET = False
    S3_SERVER_SIDE_ENCRYPTION = "AES256"
    S3_BUCKET = "quicktrust-evidence"
    S3_REPORTS_BUCKET = "quicktrust-reports"


@pytest.fixture
def storage_module(monkeypatch):
    from app.core import storage

    storage._client = None
    storage._available = False
    storage._ensured_buckets.clear()
    monkeypatch.setattr(storage, "get_settings", lambda: FakeSettings())
    return storage


def test_upload_file_uses_boto3_s3_put_object(storage_module, monkeypatch):
    fake_client = FakeS3Client()
    monkeypatch.setattr(storage_module.boto3, "client", lambda *args, **kwargs: fake_client)

    object_path = storage_module.upload_file(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
        data=b"hello",
        content_type="text/plain",
    )

    assert object_path == "quicktrust-evidence/evidence/org/file.txt"
    assert fake_client.head_bucket_calls == ["quicktrust-evidence"]
    assert len(fake_client.put_object_calls) == 1
    put_call = fake_client.put_object_calls[0]
    assert put_call["Bucket"] == "quicktrust-evidence"
    assert put_call["Key"] == "evidence/org/file.txt"
    assert put_call["Body"] == b"hello"
    assert put_call["ContentType"] == "text/plain"
    assert put_call["Metadata"]["sha256"]
    assert put_call["ServerSideEncryption"] == "AES256"


def test_upload_file_falls_back_when_sse_is_not_supported(storage_module, monkeypatch):
    fake_client = FakeS3Client(reject_sse=True)
    monkeypatch.setattr(storage_module.boto3, "client", lambda *args, **kwargs: fake_client)

    object_path = storage_module.upload_file(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
        data=b"hello",
        content_type="text/plain",
    )

    assert object_path == "quicktrust-evidence/evidence/org/file.txt"
    assert len(fake_client.put_object_calls) == 2
    assert fake_client.put_object_calls[0]["ServerSideEncryption"] == "AES256"
    assert "ServerSideEncryption" not in fake_client.put_object_calls[1]


def test_missing_bucket_is_created_only_when_enabled(storage_module, monkeypatch):
    class CreateBucketSettings(FakeSettings):
        S3_CREATE_BUCKET = True

    fake_client = FakeS3Client(missing_bucket=True)
    monkeypatch.setattr(storage_module, "get_settings", lambda: CreateBucketSettings())
    monkeypatch.setattr(storage_module.boto3, "client", lambda *args, **kwargs: fake_client)

    storage_module.upload_file(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
        data=b"hello",
        content_type="text/plain",
    )

    assert fake_client.create_bucket_calls == [
        {
            "Bucket": "quicktrust-evidence",
            "CreateBucketConfiguration": {"LocationConstraint": "us-west-2"},
        }
    ]


def test_presigned_download_and_delete_use_s3_api(storage_module, monkeypatch):
    fake_client = FakeS3Client()
    monkeypatch.setattr(storage_module.boto3, "client", lambda *args, **kwargs: fake_client)

    url = storage_module.get_presigned_url(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
    )
    response = storage_module.download_file(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
    )
    storage_module.delete_file(
        bucket="quicktrust-evidence",
        object_name="evidence/org/file.txt",
    )

    assert url == "https://signed.example/quicktrust-evidence/evidence/org/file.txt"
    assert fake_client.presigned_calls == [
        (
            "get_object",
            {"Bucket": "quicktrust-evidence", "Key": "evidence/org/file.txt"},
            3600,
        )
    ]
    assert response is not None
    assert response.headers["content-type"] == "text/plain"
    assert b"".join(response.stream(4)) == b"stored-data"
    response.close()
    response.release_conn()
    assert fake_client.delete_object_calls == [
        {"Bucket": "quicktrust-evidence", "Key": "evidence/org/file.txt"}
    ]
