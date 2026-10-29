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

### Database schema alignment

If seeding reports `column frameworks.is_active does not exist` even though
Alembic reports revision `0012`, upgrade to `0013` before retrying seeding:

```bash
docker compose exec -T postgres pg_dump -U quicktrust -d quicktrust -Fc > /tmp/quicktrust-before-0013.dump
docker compose run --rm api alembic upgrade head
docker compose run --rm api python -m seeds.run_seeds
```

Revision `0013` adds the application columns and tables omitted by earlier
migrations. It also supports databases where a failed seed run already created
some tables. Legacy columns are retained; known legacy values are copied to the
current fields. Old records without a known code receive a `legacy-<id>` code
that should not be interpreted as a real compliance requirement identifier.
PostgreSQL JSON text is converted to JSONB; invalid legacy JSON aborts the
transaction rather than being discarded. This migration is forward-only: use
the pre-upgrade backup if rollback is required.

The PostgreSQL regression test creates and removes isolated schemas in a test
database. It verifies clean/partially seeded upgrades, legacy data preservation,
and all 20 seed stages including a repeated seed run:

```bash
cd backend
QT_SCHEMA_TEST_DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/test_db python tests/test_schema_alignment_regression.py
```

### Application checks

```bash
cd backend
pytest -v
cd ../frontend
pnpm test
pnpm build
```


## QT-006: organization admins and platform staff

`User.role = super_admin` is the existing **organization administrator** role.
It no longer grants cross-organization access. The UI/API role string is retained
for compatibility. Platform staff additionally require `users.is_platform_admin = true`.
Signup, tenant provisioning, invitations, user creation, and user updates cannot
set that privilege. Customer admins retain settings and member management for their
own organization. Tenant directory/provisioning, shared framework writes, global
organization creation, and auditor verification require platform privilege.

Migration `0016` defaults **all existing and new accounts** to
`is_platform_admin = false`. No legacy super-admin account is automatically trusted
as staff, because public registration previously assigned that role. Customer accounts
keep their organization permissions. Permissions are read from the database on every
JWT/API-key request, so existing sessions cannot retain the old cross-tenant bypass.
Do not roll back to the old authorization code after this migration.

Apply the migration and deploy the new API together during a maintenance window.
For local Compose, stop the API before pulling so the development reload does not
load the new model before the migration. The default Compose file bind-mounts
`./backend` into `/app`; no image rebuild is needed for this backend-only change:

```bash
docker compose stop api
git pull --ff-only origin bug-fixes
docker compose run --rm --no-deps api alembic upgrade head
docker compose up -d --no-deps api
```

Only after independently verifying an account belongs to authorized platform staff,
a database operator may grant the separate privilege. Use that account's exact UUID;
never promote all existing super-admin users or select the first signup. For example,
run this SQL through the approved database administration channel (replace the UUID):

```sql
BEGIN;
UPDATE users
SET is_platform_admin = true, updated_at = CURRENT_TIMESTAMP
WHERE id = '<approved-staff-user-uuid>' AND is_active = true
RETURNING id, role, is_platform_admin;
COMMIT;
```

Record the approval and account UUID in the deployment record. Revoke with the same
scoped update using `false`. The next authenticated request sees the change.
Platform staff accounts cannot be modified by customer member-management/SCIM APIs
or moved between organizations through invitation acceptance.

Local verification: register two separate organizations; both owners can list their
own members (200), but foreign member lists/organization reads and writes return 403.
An employee still receives 403 for member listing/invitation creation. Customer
admins receive 403 from `/api/v1/tenants`, and attempts to submit
`is_platform_admin` in registration/user/invitation payloads return 422. A customer
admin may invite another organization admin; this does not grant platform access.
Compliance managers cannot issue administrator invitations, and invitation acceptance
rechecks that the issuer is still active and authorized.
