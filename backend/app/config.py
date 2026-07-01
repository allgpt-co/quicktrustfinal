import logging

from pydantic import model_validator
from pydantic_settings import BaseSettings
from functools import lru_cache

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # App
    APP_NAME: str = "QuickTrust"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = ""
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"

    # Database — defaults to SQLite for local dev, use postgresql+asyncpg://... for production
    # For TLS: set DATABASE_URL to postgresql+asyncpg://user:pass@host:5432/db?ssl=require
    DATABASE_URL: str = "sqlite+aiosqlite:///./quicktrust.db"
    DATABASE_SSL_CA: str = ""  # Path to CA cert (e.g. /app/rds-combined-ca-bundle.pem)

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Keycloak
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "quicktrust"
    KEYCLOAK_CLIENT_ID: str = "quicktrust-api"
    KEYCLOAK_CLIENT_SECRET: str = ""
    KEYCLOAK_ADMIN_USER: str = "admin"
    KEYCLOAK_ADMIN_PASSWORD: str = ""

    # Amazon S3 object storage. Local development can set S3_ENDPOINT_URL to a
    # MinIO or LocalStack endpoint while using the same boto3 code path.
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_SESSION_TOKEN: str = ""
    AWS_REGION: str = "us-east-1"
    S3_ENDPOINT_URL: str = ""
    S3_BUCKET: str = "quicktrust-evidence"
    S3_REPORTS_BUCKET: str = "quicktrust-reports"
    S3_FORCE_PATH_STYLE: bool = False
    S3_CREATE_BUCKET: bool = False
    S3_SERVER_SIDE_ENCRYPTION: str = "AES256"

    # LiteLLM
    LITELLM_MODEL: str = "gpt-4o-mini"
    OPENAI_API_KEY: str = ""

    # Prowler
    PROWLER_OUTPUT_DIR: str = "/tmp/prowler-output"
    PROWLER_TIMEOUT_SECONDS: int = 3600

    # Field-level encryption (generate: python -c "import os; print(os.urandom(32).hex())")
    FIELD_ENCRYPTION_KEY: str = ""
    FIELD_HMAC_KEY: str = ""

    # SMTP email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "notifications@quicktrust.dev"
    SMTP_USE_TLS: bool = True

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        """Require real secret values in production."""
        required_secret_fields = (
            "SECRET_KEY",
            "KEYCLOAK_CLIENT_SECRET",
            "KEYCLOAK_ADMIN_PASSWORD",
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_REGION",
            "S3_BUCKET",
            "S3_REPORTS_BUCKET",
        )
        insecure_values = {
            "change-me-in-production",
            "quicktrust-api-secret",
            "quicktrust_dev",
            "quicktrust_redis_dev",
            "admin",
            "changeme123",
        }
        if self.APP_ENV == "production":
            invalid_fields = [
                field_name
                for field_name in required_secret_fields
                if not getattr(self, field_name)
                or getattr(self, field_name) in insecure_values
            ]
            if invalid_fields:
                fields = ", ".join(invalid_fields)
                raise ValueError(
                    f"CRITICAL: production secret values must be set to strong, "
                    f"unique values before deploying: {fields}"
                )
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
