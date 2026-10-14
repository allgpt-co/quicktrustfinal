FROM python:3.12-slim AS base

WORKDIR /app

ARG BUILD_SHA=unknown
ENV BUILD_SHA=${BUILD_SHA}
LABEL org.opencontainers.image.revision=${BUILD_SHA}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget gnupg unzip \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" --uid 1001 appuser

COPY pyproject.toml ./

RUN pip install --no-cache-dir -e .

# Semgrep (SAST code scanner) + Checkov (IaC scanner)
# Note: Prowler is omitted from dev builds — it pulls ~2GB of cloud SDKs (AWS/Azure/GCP).
# Install it separately or use a dedicated Prowler container for cloud security scans.
RUN pip install --no-cache-dir semgrep checkov

COPY . .

RUN chown -R appuser:appuser /app

FROM base AS development
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS production
USER appuser
CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4"]
