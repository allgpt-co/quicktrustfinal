# QuickTrust audit: QT-001 through QT-004

## Scope and findings

The audit sheet describes an older Prisma/Pinecone implementation. These changes
address the current FastAPI/SQLAlchemy application. A passing local test is not
proof that the deployed environment uses the same code or configuration.

| Finding | Current result | Evidence |
| --- | --- | --- |
| QT-001 | Reported default-secret fallback not reproduced; existing protections retained | Production settings reject missing, known placeholder and short secrets. Protected API rejects missing, malformed, wrongly signed and expired tokens. |
| QT-002 | Fixed organization and bucket authorization in file routes | Ordinary users cannot upload, sign downloads, or delete for another organization. Only the configured evidence bucket and the exact `org_id/` prefix are accepted. Existing explicit platform super-admin override remains. |
| QT-003 | No leakage reproduced in the tested embedding search path | API rejects other-organization searches. Database-filtering test returns only the selected tenant's vectors; an empty tenant receives nothing. These tests do not cover every AI feature. |
| QT-004 | Current Auto-fill processed all AI batches within an HTTP request; now queued | POST returns 202 and persisted job metadata without calling the LLM. The worker processes batches and the frontend polls progress, refreshes saved answers, and offers retry on failure. |

## Auto-fill behavior

- `POST /api/v1/organizations/{org_id}/questionnaires/{id}/auto-fill` returns
  **202** with `{id,status,current_step,total_steps,step_name,output_data,error_message}`.
  This replaces the old 200/message contract. Deploy the frontend and backend together.
- `GET` at the same URL returns the latest job or `null`. It verifies both the
  caller's organization access and the questionnaire's organization.
- The existing `workflow_executions` table is the durable queue. Each API process
  runs one worker; PostgreSQL `FOR UPDATE SKIP LOCKED` prevents multiple workers
  from claiming the same job. A questionnaire row lock deduplicates concurrent
  submissions. PostgreSQL is required for these multi-process guarantees.
- Jobs execute with their own database sessions and tenant context. Requests do
  not pass database sessions into background tasks.
- A job has a 15-minute execution deadline. Graceful shutdown marks the active
  job failed. After an abrupt process loss, another worker marks it failed after
  16 minutes; queued jobs remain available. Failed jobs are **not automatically
  retried**. Users may retry; already committed response rows are skipped.
- Matching and each completed AI batch update progress. A provider failure fails
  the job without exposing provider error details; earlier committed answers stay
  available. Completion may produce zero answers if the model cannot answer.
- Questionnaire editing, response mutation, and deletion are blocked while a job
  is pending or running. The UI disables those controls during processing.
- The page reloads the latest job after navigation and refreshes answers and counts
  at completion/failure. Generated response rows are displayed alongside original
  questions. Both legacy and seeded question field names are supported.
- The generic workflow detail route also checks the requested organization, so
  it cannot bypass the new job-status route's tenant check.

## Included local setup corrections

The branch already contained migration 0013 and its schema regression test. They
are retained, including its forward-only rollback policy. Migration 0014 adds and
backfills the framework update timestamp. Questionnaire timestamps already have
database defaults, and the existing workflow table holds the new jobs. The frontend content loader now works
from both the repository root and Docker's `/app` frontend working directory.
The development image copies the Python package before editable installation and
includes pytest; production does not gain test-runner dependencies.

Local `.env` values and Docker image overrides used on an individual developer's
computer are not committed. No secrets are included in this change.

## Review and deployment

1. Back up the database before migration 0013. Read its forward-only downgrade
   warning; use a backup restore for rollback rather than dropping populated tables.
2. Apply `alembic upgrade head` before deploying the worker/API. Expected head: 0014.
3. Deploy backend and frontend together, then verify 202 submission, status polling,
   completion, and persisted answers using a test organization.
4. QT-002 tests mock storage operations. An actual harmless-file test with two
   ordinary test accounts is still required to validate storage configuration.
5. Production JWT settings and real provider behavior remain deployment checks.
   Tests never call a paid AI provider.

## Repeatable verification

Development API container (built with target `development`):

```bash
docker compose run --rm api python -m pytest -q \
  tests/test_production_hardening.py tests/test_auth.py \
  tests/test_audit_auth_storage_search.py tests/test_storage_s3.py \
  tests/test_questionnaires.py tests/test_questionnaire_jobs.py
```

PostgreSQL tests create and drop their own randomly named schemas in a disposable
**test database**, including full migrations and repeated seeding. Do not point
this command at a production database.

```bash
cd backend
QT_SCHEMA_TEST_DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST/TEST_DB \
  python tests/test_schema_alignment_regression.py
```

Frontend:

```bash
cd frontend
pnpm install --frozen-lockfile
pnpm exec tsc --noEmit
pnpm test -- tests/auto-fill-status.test.tsx tests/auto-fill-polling.test.tsx
```

## Validation performed on this branch

- 29 targeted backend tests passed (authentication, production settings, mocked
  file authorization, tenant search, questionnaire API, queue lifecycle and S3 helpers).
- PostgreSQL migration/seed regression tests passed in disposable schemas. The
  queue integration test was rerun against final migration head 0014 and passed:
  concurrent enqueue deduplication, exclusive worker claims and saved answers.
- Four frontend tests passed for accessible status messages and polling/cache updates.
  TypeScript checking and `git diff --check` passed.
- Playwright with mocked API responses verified desktop and 390px mobile layouts,
  queued/running states, recovery after reload, completed answers, failure/retry
  controls and keyboard dismissal of the mobile navigation. Screenshots were
  reviewed. The shared sidebar now collapses on mobile so the page remains usable.
- These checks do not constitute production verification or a live AI/storage test.
  An existing third-party analytics script generated a CSP warning during browser
  testing; it did not prevent the questionnaire flow.
