import logging
from urllib.parse import urlparse

from pydantic import model_validator
from pydantic_settings import BaseSettings
from functools import lru_cache

logger = logging.getLogger(__name__)


def _is_localhost_url(value: str) -> bool:
    try:
        hostname = urlparse(value).hostname
    except Exception:
        return False

    return hostname in {"localhost", "127.0.0.1", "0.0.0.0"} or (
        hostname is not None and hostname.endswith(".localhost")
    )


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

    # Application-managed authentication
    JWT_ISSUER: str = "quicktrust"
    JWT_AUDIENCE: str = "quicktrust-api"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_EXPIRE_MINUTES: int = 60
    AUTH_COOKIE_SECURE: bool = False
    AUTH_COOKIE_DOMAIN: str = ""

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

    # Amazon Bedrock / Anthropic Claude Sonnet (routed through LiteLLM)
    BEDROCK_ENABLED: bool = False
    BEDROCK_MODEL_ID: str = ""
    BEDROCK_INPUT_COST_PER_MILLION: float = 0.0
    BEDROCK_OUTPUT_COST_PER_MILLION: float = 0.0

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
        """Require real production values in production."""
        if self.BEDROCK_ENABLED:
            model_id = self.BEDROCK_MODEL_ID.lower()
            if (
                model_id.startswith("replace-with")
                or "anthropic" not in model_id
                or "claude" not in model_id
                or "sonnet" not in model_id
            ):
                raise ValueError(
                    "BEDROCK_MODEL_ID must identify an Anthropic Claude Sonnet model "
                    "or inference profile when BEDROCK_ENABLED is true"
                )
            if (
                self.BEDROCK_INPUT_COST_PER_MILLION <= 0
                or self.BEDROCK_OUTPUT_COST_PER_MILLION <= 0
            ):
                raise ValueError(
                    "BEDROCK_INPUT_COST_PER_MILLION and "
                    "BEDROCK_OUTPUT_COST_PER_MILLION must be positive when "
                    "BEDROCK_ENABLED is true"
                )

        required_secret_fields = (
            "SECRET_KEY",
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
            "replace-with-random-32-byte-secret",
        }
        if self.APP_ENV == "production":
            messages = []
            invalid_fields = [
                field_name
                for field_name in required_secret_fields
                if not getattr(self, field_name)
                or getattr(self, field_name) in insecure_values
            ]
            if invalid_fields:
                fields = ", ".join(invalid_fields)
                messages.append(
                    f"CRITICAL: production secret values must be set to strong, "
                    f"unique values before deploying: {fields}"
                )

            if len(self.SECRET_KEY) < 32:
                messages.append(
                    "CRITICAL: SECRET_KEY must be at least 32 characters in production"
                )
            if not self.AUTH_COOKIE_SECURE:
                messages.append(
                    "CRITICAL: AUTH_COOKIE_SECURE must be true in production"
                )

            localhost_fields = []
            if any(_is_localhost_url(origin) for origin in self.cors_origins_list):
                localhost_fields.append("CORS_ORIGINS")
            if localhost_fields:
                fields = ", ".join(localhost_fields)
                messages.append(
                    f"CRITICAL: production network settings must not use localhost: {fields}"
                )

            if messages:
                raise ValueError("; ".join(messages))
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
