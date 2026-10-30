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


## QT-007: questionnaire Auto-fill usage records

Migration `0018` adds `ai_usage_events`. Each attempted Auto-fill provider call gets
one durable row containing organization/user/questionnaire/job IDs, batch number,
model, provider input/output token counts, captured pricing rates, and estimated
cost in integer micro-USD. No prompts, answers, emails, or document text are stored
in the ledger. Questionnaire/job/user references are snapshots so deleting a
questionnaire does not erase its usage history.

A `started` row is committed before calling the provider. The same row is finalized
once, before JSON parsing or answer persistence. Repeated finalization cannot count
a call twice. A retry that makes another provider invocation gets a new row because
it can incur new cost; already answered questions are skipped. Provider usage is
retained even when JSON parsing or answer persistence fails. A crash, cancellation,
or failure to finalize may leave `started`, meaning the outcome needs reconciliation.
A failed provider call or missing provider token data is `unknown`, not free usage.
Local disabled-Bedrock calls are explicitly `mock` with zero cost and must be excluded
from paid-usage reports.

`reported` rows contain actual provider token counts. Estimated cost uses
`BEDROCK_INPUT_COST_PER_MILLION` and `BEDROCK_OUTPUT_COST_PER_MILLION` for the
configured `BEDROCK_MODEL_ID`, captured at call start. Missing/zero prices or a model
mismatch yield NULL cost, not zero. The arithmetic uses Decimal and rounds once at
micro-USD precision. These are estimates, not invoice amounts: cache discounts,
provider-internal retries, and spend whose usage response was lost are not inferred.
Do not reconstruct unknown usage as zero or promise exact invoice reconciliation.

Scope: this change meters questionnaire Auto-fill. The existing agent-run Redis
budget counter/UI and its legacy 50/50 cost estimator are unchanged; the new ledger
is not yet a billing/subscription/quota system or an all-product AI usage dashboard.
Aggregate ledger data by `org_id`, UTC period, and status; surface unknown-cost rows
separately rather than treating a partial known-cost total as complete.

Apply `alembic upgrade head` with the updated API. Keep this branch separate from
PR #19 until that prerequisite is merged. For the default local Compose bind mount:

```bash
docker compose stop api
git switch qt-007-ai-usage
git pull --ff-only origin qt-007-ai-usage
docker compose run --rm --no-deps api alembic upgrade head
docker compose up -d --no-deps api
```

Run the focused tests without real AWS/Bedrock access or application database writes:

```bash
docker compose run --rm --no-deps -w /tmp -e PYTHONPATH=/app -e DATABASE_URL=sqlite+aiosqlite:////tmp/qt007-app.db -e BEDROCK_ENABLED=false api python -m pytest /app/tests/test_ai_usage.py -q
```

The development image must contain pytest (the Dockerfile development target does).
Tests replace the provider with mocks and use a temporary SQLite database inside the
removed test container. Test prices are synthetic, not current vendor rates. Production
verification against Bedrock/provider invoices remains a separate follow-up.

Validation limitation: the broader partial-seed schema regression fails when all
application models are loaded, due to 22 existing missing columns across
notifications, notification_preferences, slack_webhook_configs, auditor_profiles,
and embeddings. This was reproduced on the unchanged QT-006 base (`cb10355`)
with `app.main` imported before that test. It requires a separate schema repair;
the Auto-fill usage migration does not change those tables.

## QT-008: plan/subscription foundation

Migration `0019` follows `0018` and creates `billing_plans` and
`billing_subscriptions`. It does not assign plans, start trials, mark organizations
as paying, or change access to existing product routes. Existing and new
organizations without a subscription return `configured: false`, reason
`unconfigured`. There are no invented prices, trial durations, or package limits.

Plans contain a unique code, display name, named resource limits, and boolean
features. Plan definitions are immutable through this API: create a new code for
a revised package, then explicitly move contracted organizations. This prevents a
package edit from silently changing all existing customer agreements. An inactive
plan cannot be newly assigned; existing assignments retain their agreement.
Subscriptions record the plan, status, billing interval, explicit UTC period,
optional trial end and contract reference, and per-organization overrides. Only
manual agreements are supported here; Stripe/webhooks/invoicing remain separate.
There is at most one current subscription per organization. Changes retain
before/after snapshots in the existing audit log in the same database transaction.

API paths (all under `/api/v1`):

- `POST /admin/billing/plans`: platform staff only; create a plan.
- `GET /admin/billing/plans?offset=0&limit=50`: platform staff only; list plans.
- `PUT /admin/organizations/{org_id}/subscription`: platform staff only; fully
  replace subscription configuration. Send `expected_version: 0` to create, or the
  current returned `version` to update. Concurrent or stale writes return 409.
- `GET /organizations/{org_id}/billing/subscription`: the organization's
  `super_admin` or platform staff; returns subscription (null if unconfigured)
  and resolved entitlements. Employees/managers cannot read contract details.
- `GET /organizations/{org_id}/entitlements`: internal organization members or
  platform staff; exposes only resolved feature/limit information, not contract
  references. Foreign-organization access is rejected for customer users,
  including the customer `super_admin` role.

Only the explicit `is_platform_admin` privilege grants write access. Customers
cannot grant themselves a plan using organization settings or request-body fields.
Do not promote customer accounts to platform staff for routine testing; the
isolated automated tests exercise both roles without changing real users.

Example plan payload (illustrative test data, not commercial commitments):

```json
{
  "code": "local_test_v1",
  "name": "Local Test Plan",
  "limits": {"seats": 5, "documents": 10},
  "features": {"questionnaire_export": true}
}
```

A subscription PUT requires `plan_id`, `expected_version`, `status`,
`billing_interval` (`month` or `year`), `current_period_start`, and
`current_period_end` as timezone-aware ISO timestamps. `trialing` also requires
`trial_ends_at` within that period. Optional `limit_overrides` and
`feature_overrides` merge by key over the plan. Omitted keys inherit; explicit 0
and false override; a null limit means no configured cap. Do not treat a missing
feature as enabled. PUT is a full replacement, so omitted overrides are cleared.

`billing_service.get_entitlements` is the shared resolver. Only active or unexpired
trialing subscriptions within their explicit period return `access_allowed: true`.
Other statuses and future/expired periods return false and disable feature grants.
These are configuration evaluations, not middleware: `enforcement_enabled: false`
explicitly reports that product routes are not yet gated. Limits are configuration,
not current consumption or concurrency-safe quota reservations. Seats, AI calls,
upload gates, signup plan assignment, renewal jobs, payments, and billing UI belong
to separate findings. The resolver never claims a payment was actually received.

After obtaining the updated code, stop the API, apply `alembic upgrade head`,
confirm `alembic current` reports `0019 (head)`, then restart the API. Migration
0019 is forward-only to avoid accidentally deleting commercial records.

Run the isolated test suite (no AWS, Stripe, or production database credentials):

```bash
docker compose run --rm --no-deps -w /tmp \
  -e PYTHONPATH=/app \
  -e DATABASE_URL=sqlite+aiosqlite:////tmp/qt008-app.db \
  -e BEDROCK_ENABLED=false \
  api python -m pytest /app/tests/test_billing.py -q -p no:cacheprovider
```

The tests cover platform-only writes, tenant isolation, employee access, unknown
plans, overrides, stale writes, validation, expiry, audit atomicity, and unchanged
settings access for unconfigured organizations. Separate PostgreSQL migration
regressions cover upgrade from 0018, seed-created tables, database constraints,
and concurrent subscription updates. The broader pre-existing schema issue
noted under QT-007 remains outside this change.

## QT-009: durable usage events and counters

Migration `0020` adds `usage_events`, `usage_counters`, and nullable period-snapshot
fields on `ai_usage_events`. Apply it before restarting the updated API/worker.
No prices, invoices, or enforcement rules are introduced. The existing Redis agent
budget counter is not replaced or represented as complete by this change.

`usage_service.append_event` is the internal write primitive. Its caller owns the
transaction and must roll back on error. A receipt is unique by organization,
resource kind, and idempotency key. An identical retry preserves the original
receipt/period and does not increment again; reuse with different consumption
raises an error. The receipt insert and counter upsert share the same transaction
as the action they measure. PostgreSQL increments use `ON CONFLICT DO UPDATE`,
not a read/modify/write sequence. There is no public usage-write endpoint.

Currently connected sources:

- `LLM_COMPLETION`: one receipt per finalized Auto-fill provider invocation, linked
  to its existing `ai_usage_events` ID. This is an accounting projection, not an
  additional charge. It counts attempted calls, including failures with unknown
  consumption. Costs/tokens are recorded only here, so answer/questionnaire
  counters do not duplicate them. `started` calls remain pending reconciliation.
- `QUESTION_ANSWERED`: one receipt per persisted, server-generated AI answer, in
  the same transaction as that answer. Provider calls with invalid output or
  failed answer saves still retain their call cost but generate no answer count.
- `QUESTION_MATCHED`: keyword/control/policy matches count separately from AI
  answers, with no additional provider cost. Client-created answer rows do not
  constitute proof of metered processing.
- `QUESTIONNAIRE_PROCESSED`: once per questionnaire ID, on the first successful
  Auto-fill completion with a surviving answer backed by a non-mock processing
  receipt. Retries, including completion after earlier answer saves, do not count
  that questionnaire again, even across periods. This is a defined operational
  metric, not a finalized commercial charging policy. Empty/unanswerable,
  manual-only, legacy-only, or mock-only results do not qualify.

The generic service also supports embedding, vector query/upsert, email, and signed
storage-byte events, but those call sites are not connected in this change. Storage
quantities are deltas within a period, not a current-storage gauge. Other AI agents,
real provider invoice reconciliation, alerts, quotas, and billing UI remain separate
work. Do not claim complete product-wide metering based on these counters.

Period rules:

- Use the organization's configured subscription period when the event timestamp
  falls in `[current_period_start, current_period_end)`, regardless of its status;
  already-performed work must still be recorded for a suspended organization.
- Otherwise use the UTC calendar month, labeled `calendar_month` rather than
  implying an active subscription. Never reset old counters on renewal.
- AI call periods are captured before the call. Its answer receipts use that same
  start timestamp and period. A long-running call remains in its original bucket
  if staff renews/changes the subscription before the response returns. Keyword
  answers use their save time; questionnaire completion uses its completion time.
- Period start/end/source are immutable receipt attributes. Editing a subscription
  does not rewrite old consumption. The API lists every stored bucket, including
  previous bounds, so mid-period contract edits do not hide historical usage.

Counters expose event count, quantity, **known** input/output token totals and
micro-USD cost, plus unknown-token and unpriced-event counts. A known subtotal of
zero with unpriced events is not proof of zero spend. Mock receipts are retained
for diagnosis and excluded entirely from consumption counters. Business-unit
receipts have zero *additional* provider cost; their associated call carries it.
Receipt references survive questionnaire/answer deletion.

Read `GET /api/v1/organizations/{org_id}/billing/usage?offset=0&limit=50` as the
organization administrator or platform staff. It returns stored counters,
`next_offset`, pending AI calls, finalized AI calls awaiting projection, excluded
mock-event count, and coverage/enforcement information. Foreign-organization
requests and non-admin customer roles are rejected. Quantities are not invoices
and do not themselves block any product action.

### Existing AI records

Migration 0020 leaves previous finalized AI records intact. Their new counters are
not assumed to exist: the read API reports `unprojected_ai_calls`. An operator can
project an authorized organization's legacy AI records in bounded, resumable
batches after migration:

```bash
docker compose run --rm --no-deps api python -m app.scripts.backfill_ai_usage \
  --org-id YOUR_ORGANIZATION_UUID --batch-size 100 --max-batches 10
```

This command writes the configured application database; it is not the isolated
test command below. Repeat it if it reports remaining finalized rows. Existing
snapshots are respected. Older AI records without snapshots are explicitly placed
in `legacy_calendar_month`; their historical subscription is unknown and is never
inferred from the current plan. Started calls and old answer/questionnaire business
units are not reconstructed. Do not treat historical coverage as complete.

### Local verification without provider credentials

After pulling `bug-fixes`, stop the API, run `alembic upgrade head`, verify
`alembic current` shows `0020 (head)`, and restart the API. Run the isolated tests:

```bash
docker compose run --rm --no-deps -w /tmp \
  -e PYTHONPATH=/app \
  -e DATABASE_URL=sqlite+aiosqlite:////tmp/qt009-app.db \
  -e BEDROCK_ENABLED=false \
  api python -m pytest /app/tests/test_usage.py -q -p no:cacheprovider
```

Tests use synthetic usage and mocked AI responses. Separate PostgreSQL regressions
exercise concurrent duplicate/distinct writes, counter failure/rollback, migration
from 0019, seed-created tables, repeatable legacy backfill, concurrent provider
finalization, and queue integration. The pre-existing broader schema discrepancy
noted under QT-007 is unchanged.
