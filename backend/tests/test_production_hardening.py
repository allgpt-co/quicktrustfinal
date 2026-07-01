import pytest
from pydantic import ValidationError

from app.config import Settings
from app.services.user_service import _generate_temporary_password


def valid_production_settings(**overrides: str) -> dict[str, str]:
    settings = {
        "APP_ENV": "production",
        "SECRET_KEY": "super-secret-production-key",
        "KEYCLOAK_URL": "https://keycloak.quicktrustapp.com",
        "KEYCLOAK_CLIENT_SECRET": "super-secret-keycloak-client-secret",
        "KEYCLOAK_ADMIN_PASSWORD": "super-secret-keycloak-admin-password",
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
            KEYCLOAK_CLIENT_SECRET="",
            KEYCLOAK_ADMIN_PASSWORD="",
            AWS_ACCESS_KEY_ID="",
            AWS_SECRET_ACCESS_KEY="",
            AWS_REGION="",
            S3_BUCKET="",
            S3_REPORTS_BUCKET="",
        )

    message = str(exc_info.value)
    assert "SECRET_KEY" in message
    assert "KEYCLOAK_CLIENT_SECRET" in message
    assert "KEYCLOAK_ADMIN_PASSWORD" in message
    assert "AWS_ACCESS_KEY_ID" in message
    assert "AWS_SECRET_ACCESS_KEY" in message
    assert "AWS_REGION" in message
    assert "S3_BUCKET" in message
    assert "S3_REPORTS_BUCKET" in message


def test_production_rejects_known_development_secret_values() -> None:
    with pytest.raises(ValidationError):
        Settings(
            APP_ENV="production",
            SECRET_KEY="change-me-in-production",
            KEYCLOAK_CLIENT_SECRET="quicktrust-api-secret",
            KEYCLOAK_ADMIN_PASSWORD="admin",
            AWS_ACCESS_KEY_ID="quicktrust_dev",
            AWS_SECRET_ACCESS_KEY="quicktrust_dev",
            AWS_REGION="us-east-1",
            S3_BUCKET="quicktrust-evidence",
            S3_REPORTS_BUCKET="quicktrust-reports",
        )


def test_production_rejects_localhost_keycloak_url() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(**valid_production_settings(KEYCLOAK_URL="http://localhost:8080"))

    assert "KEYCLOAK_URL" in str(exc_info.value)


def test_production_rejects_localhost_cors_origins() -> None:
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            **valid_production_settings(
                CORS_ORIGINS="https://quicktrustapp.com,http://localhost:3001"
            )
        )

    assert "CORS_ORIGINS" in str(exc_info.value)


def test_generated_temporary_password_is_not_hardcoded() -> None:
    first = _generate_temporary_password()
    second = _generate_temporary_password()

    assert first != "changeme123"
    assert second != "changeme123"
    assert first != second
    assert first.endswith("Aa1!")
    assert len(first) >= 16


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
async def test_production_token_decode_does_not_retry_localhost_issuer(monkeypatch) -> None:
    from jose import JWTError

    from app.core import security
    from app.core.exceptions import UnauthorizedError

    issuers: list[str] = []

    async def fake_get_jwks() -> dict:
        return {"keys": [{"kid": "test-key"}]}

    def fake_decode(*args, issuer: str, **kwargs) -> dict:
        issuers.append(issuer)
        raise JWTError("bad issuer")

    monkeypatch.setattr(security, "get_jwks", fake_get_jwks)
    monkeypatch.setattr(security.jwt, "get_unverified_header", lambda token: {"kid": "test-key"})
    monkeypatch.setattr(security.jwt, "decode", fake_decode)
    monkeypatch.setattr(security.settings, "APP_ENV", "production")
    monkeypatch.setattr(security.settings, "KEYCLOAK_URL", "https://keycloak.quicktrustapp.com")

    with pytest.raises(UnauthorizedError):
        await security.decode_token("token")

    assert issuers == ["https://keycloak.quicktrustapp.com/realms/quicktrust"]
