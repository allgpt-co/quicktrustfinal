import uuid

import pytest
from pydantic import ValidationError

from app.config import Settings


def valid_production_settings(**overrides) -> dict:
    settings = {
        "APP_ENV": "production",
        "SECRET_KEY": "a-strong-production-signing-key-over-32-characters",
        "AUTH_COOKIE_SECURE": True,
        "AWS_ACCESS_KEY_ID": "AKIAPRODUCTION",
        "AWS_SECRET_ACCESS_KEY": "super-secret-aws-secret",
        "AWS_REGION": "us-east-1",
        "S3_BUCKET": "quicktrust-production-evidence",
        "S3_REPORTS_BUCKET": "quicktrust-production-reports",
        "CORS_ORIGINS": "https://quicktrustapp.com",
    }
    settings.update(overrides)
    return settings


def test_production_requires_real_secret_values() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            APP_ENV="production",
            SECRET_KEY="",
            AUTH_COOKIE_SECURE=False,
            AWS_ACCESS_KEY_ID="",
            AWS_SECRET_ACCESS_KEY="",
            AWS_REGION="",
            S3_BUCKET="",
            S3_REPORTS_BUCKET="",
        )

    message = str(exc_info.value)
    for field in (
        "SECRET_KEY", "AUTH_COOKIE_SECURE", "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY", "AWS_REGION", "S3_BUCKET", "S3_REPORTS_BUCKET",
    ):
        assert field in message


def test_production_rejects_known_development_secret_values() -> None:
    with pytest.raises(ValidationError):
        Settings(
            **valid_production_settings(
                SECRET_KEY="replace-with-random-32-byte-secret",
                AWS_ACCESS_KEY_ID="quicktrust_dev",
                AWS_SECRET_ACCESS_KEY="quicktrust_dev",
            )
        )


def test_production_rejects_short_signing_key() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(**valid_production_settings(SECRET_KEY="too-short"))
    assert "at least 32 characters" in str(exc_info.value)


def test_production_rejects_insecure_auth_cookie() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(**valid_production_settings(AUTH_COOKIE_SECURE=False))
    assert "AUTH_COOKIE_SECURE" in str(exc_info.value)


def test_production_rejects_localhost_cors_origins() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            **valid_production_settings(
                CORS_ORIGINS="https://quicktrustapp.com,http://localhost:3001"
            )
        )
    assert "CORS_ORIGINS" in str(exc_info.value)


@pytest.mark.asyncio
async def test_production_startup_skips_metadata_create_all(monkeypatch) -> None:
    from app import main

    class FailingEngine:
        def begin(self):
            raise AssertionError("create_all path must not run in production")

    monkeypatch.setattr(main.settings, "APP_ENV", "production")
    monkeypatch.setattr(main, "engine", FailingEngine())
    await main._create_schema_for_non_production()


@pytest.mark.asyncio
async def test_application_access_token_validates_issuer_and_audience(monkeypatch) -> None:
    from jose import jwt
    from app.core import security
    from app.core.exceptions import UnauthorizedError

    class User:
        id = uuid.uuid4()
        org_id = uuid.uuid4()
        email = "admin@example.com"
        full_name = "Admin User"
        role = "super_admin"

    monkeypatch.setattr(security.settings, "SECRET_KEY", "test-signing-key-that-is-long-enough-1234")
    monkeypatch.setattr(security.settings, "JWT_ISSUER", "quicktrust-test")
    monkeypatch.setattr(security.settings, "JWT_AUDIENCE", "quicktrust-test-api")
    token, _ = security.create_access_token(User())
    payload = await security.decode_token(token)
    assert payload["sub"] == str(User.id)
    assert payload["role"] == "super_admin"

    bad_token = jwt.encode(
        {**payload, "iss": "wrong-issuer"},
        security.settings.SECRET_KEY,
        algorithm=security.JWT_ALGORITHM,
    )
    with pytest.raises(UnauthorizedError):
        await security.decode_token(bad_token)
