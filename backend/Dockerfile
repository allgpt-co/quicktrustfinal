FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget gnupg unzip \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" --uid 1001 appuser

# --- Security Scanner Tools ---

# Trivy (container vulnerability scanner)
RUN wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor -o /usr/share/keyrings/trivy.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" > /etc/apt/sources.list.d/trivy.list \
    && apt-get update && apt-get install -y --no-install-recommends trivy \
    && rm -rf /var/lib/apt/lists/*

# Gitleaks (secret detection)
RUN wget -qO /tmp/gitleaks.tar.gz "https://github.com/gitleaks/gitleaks/releases/download/v8.21.2/gitleaks_8.21.2_linux_x64.tar.gz" \
    && tar -xzf /tmp/gitleaks.tar.gz -C /usr/local/bin gitleaks \
    && chmod +x /usr/local/bin/gitleaks \
    && rm /tmp/gitleaks.tar.gz

# Nuclei (template-based scanner)
RUN wget -qO /tmp/nuclei.zip "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.7/nuclei_3.3.7_linux_amd64.zip" \
    && unzip -o /tmp/nuclei.zip -d /usr/local/bin \
    && chmod +x /usr/local/bin/nuclei \
    && rm /tmp/nuclei.zip

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
