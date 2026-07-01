import pytest
from pydantic import ValidationError

from app.config import Settings
from app.services.user_service import _generate_temporary_password


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
