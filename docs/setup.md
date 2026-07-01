# QuickTrust — Local Development Setup

## Prerequisites

- Docker & Docker Compose
- Node.js 20+ and pnpm 9+
- Python 3.12+ (for local backend development)
- Git

## Quick Start

### 1. Clone and configure

```bash
git clone <repo-url> grcplatfrom
cd grcplatfrom
cp .env.example .env
```

### 2. Start all services

```bash
docker compose up -d
```

This starts 7 services:
- **PostgreSQL** (pgvector) — port 5432
- **Redis** — port 6379
- **MinIO** — local S3-compatible emulator, ports 9000 (API), 9001 (console)
- **Keycloak** — port 8080
- **API** (FastAPI) — port 8000
- **Web** (Next.js) — port 3000
- **Traefik** — ports 80, 8081

### 3. Run database migrations

```bash
docker compose exec api alembic upgrade head
```

### 4. Seed data

```bash
docker compose exec api python -m seeds.run_seeds
```

This loads:
- SOC 2 Type II framework (9 domains, 33 requirements)
- 25 control templates
- 20 evidence templates

### 5. Verify

- API health: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Keycloak admin: http://localhost:8080 (use KEYCLOAK_ADMIN / KEYCLOAK_ADMIN_PASSWORD from your local .env)
- Frontend: http://localhost:3000
- Local S3 emulator console: http://localhost:9001

### 6. Dev users

The committed Keycloak realm does not include demo users or passwords. Create local users through the Keycloak admin console or the application invitation/user-management flow, then assign the required realm roles.

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Running Tests

```bash
cd backend
pip install aiosqlite  # for test database
pytest -v
```

## Environment Variables

See `.env.example` for all available configuration options.

### Object Storage

Production uses Amazon S3 through boto3. Configure these variables in production:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (optional)
- `AWS_REGION`
- `S3_BUCKET` for evidence and generic uploads
- `S3_REPORTS_BUCKET` for rendered reports
- `S3_ENDPOINT_URL` should be empty for AWS S3
- `S3_FORCE_PATH_STYLE=false`
- `S3_CREATE_BUCKET=false`
- `S3_SERVER_SIDE_ENCRYPTION=AES256`

Local Docker development still starts MinIO as an S3-compatible emulator. Keep `S3_ENDPOINT_URL=http://minio:9000`, `S3_FORCE_PATH_STYLE=true`, and `S3_CREATE_BUCKET=true` locally.

## AI Agent Configuration

To use the controls generation agent with a real LLM:

1. Set `OPENAI_API_KEY` in `.env`
2. Optionally change `LITELLM_MODEL` (default: `gpt-4o-mini`)
3. The agent falls back to template-based generation if no API key is configured
