# QuickTrust — Local Development Setup

## Prerequisites

- Docker and Docker Compose
- Node.js 20+ and pnpm 9+
- Python 3.12+ for direct backend development
- Git

## Docker Quick Start

```bash
git clone <repo-url> quicktrust
cd quicktrust
cp .env.example .env
# Replace all required password/key placeholders.
docker compose up -d
docker compose exec api alembic upgrade head
docker compose exec api python -m seeds.run_seeds
```

The development stack starts six services: PostgreSQL, Redis, a local S3-compatible emulator, FastAPI, Next.js, and Traefik. The base Compose file exposes the API on `8000`, web app on `3001`, and local storage console on `9001`; the optional override may choose different host ports.

Verify:

- API health: http://localhost:8000/health
- API documentation: http://localhost:8000/docs
- Frontend: http://localhost:3001
- Local object-storage console: http://localhost:9001

## Create a Development Account

Open `/login`, select **Create account**, and enter an email, name, and policy-compliant password. The first user of a new self-registered organization receives the existing `super_admin` role. Invited users should use their invitation link; the role and organization from the invitation are preserved.

Users that existed before application-managed authentication do not have transferable password material. Use **Forgot password?** on `/login` to establish a password. Configure SMTP to deliver links; when SMTP is intentionally absent in development, the backend logs the reset URL.

## Local Development Without Docker

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

```bash
cd frontend
pnpm install
pnpm dev
```

## Authentication Configuration

- `SECRET_KEY` — strong JWT signing secret; at least 32 characters in production
- `JWT_ISSUER`, `JWT_AUDIENCE` — access-token validation values
- `ACCESS_TOKEN_EXPIRE_MINUTES` — short-lived access token lifetime (default 15)
- `REFRESH_TOKEN_EXPIRE_DAYS` — refresh-session lifetime (default 7)
- `PASSWORD_RESET_EXPIRE_MINUTES` — one-time reset-link lifetime (default 60)
- `AUTH_COOKIE_SECURE=true` — mandatory in production
- `AUTH_COOKIE_DOMAIN=.quicktrustapp.com` — production parent domain so the web route guard and API share the refresh cookie
- SMTP variables — required to deliver invitation and password setup/reset email in deployed environments

The browser never persists the access JWT. The API sets the refresh secret as an HttpOnly cookie, rotates it on refresh, and stores only its SHA-256 digest.

## Object Storage

Production uses Amazon S3 through boto3. Configure AWS credentials/role, `AWS_REGION`, `S3_BUCKET`, and `S3_REPORTS_BUCKET`; leave `S3_ENDPOINT_URL` empty, `S3_FORCE_PATH_STYLE=false`, and `S3_CREATE_BUCKET=false`. Local Docker uses the emulator endpoint with path-style access and bucket creation enabled.

## AI Agent Configuration

Set `BEDROCK_ENABLED=true`, select an Anthropic Claude Sonnet model or inference profile in `BEDROCK_MODEL_ID`, provide AWS credentials through the normal boto3 credential chain, and configure positive current input/output rates. With Bedrock disabled, local development and CI use deterministic mock responses.

## Tests

```bash
cd backend
pytest -v
cd ../frontend
pnpm test
pnpm build
```
