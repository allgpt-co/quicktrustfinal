# QuickTrust GRC Audit -- Step-by-Step Implementation Guide

**Date:** 2026-03-06
**Reference:** grcaudit.md (114 findings across 10 categories)
**Structure:** Each section maps to an audit finding with exact file paths, line numbers, code diffs, and verification steps.

---

## Table of Contents

- [Phase 1: Critical Security (Week 1)](#phase-1-critical-security-week-1)
- [Phase 2: Core Security Hardening (Weeks 2-3)](#phase-2-core-security-hardening-weeks-2-3)
- [Phase 3: Data Integrity & Schema Validation (Weeks 4-5)](#phase-3-data-integrity--schema-validation-weeks-4-5)
- [Phase 4: AI Agent Safety (Week 6)](#phase-4-ai-agent-safety-week-6)
- [Phase 5: Evidence & Compliance (Week 7)](#phase-5-evidence--compliance-week-7)
- [Phase 6: Infrastructure Hardening (Weeks 8-9)](#phase-6-infrastructure-hardening-weeks-8-9)
- [Phase 7: Frontend Security & UX (Weeks 10-11)](#phase-7-frontend-security--ux-weeks-10-11)
- [Phase 8: CI/CD & DevSecOps (Week 12)](#phase-8-cicd--devsecops-week-12)
- [Phase 9: Production Readiness (Weeks 13-14)](#phase-9-production-readiness-weeks-13-14)
- [Phase 10: Polish & Long-Term (Weeks 15+)](#phase-10-polish--long-term-weeks-15)

---

## Phase 1: Critical Security (Week 1)

### 1.1 Add Missing `asyncpg` Dependency (Audit C-3.1, Infra 3.1.1)

**Why:** Application crashes on PostgreSQL startup. Production is blocked.

**File:** `backend/pyproject.toml`

**Step 1:** Add `asyncpg` to the dependencies list at line 10:

```python
# backend/pyproject.toml - add after line 10 (after aiosqlite)
dependencies = [
    "fastapi[standard]>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "sqlalchemy[asyncio]>=2.0.36",
    "aiosqlite>=0.20.0",
    "asyncpg>=0.30.0",            # <-- ADD THIS LINE
    "alembic>=1.14.0",
    # ... rest unchanged
]
```

**Verify:**
```bash
cd backend && pip install -e . && python -c "import asyncpg; print('OK')"
```

---

### 1.2 Enable JWT Audience Verification (Audit C-2)

**Why:** Any token from the same Keycloak realm is accepted. Cross-app authentication bypass.

**File:** `backend/app/core/security.py`

**Step 1:** Replace lines 59-66 with proper audience verification:

```python
# backend/app/core/security.py - replace lines 59-66
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.KEYCLOAK_CLIENT_ID,
            issuer=issuer,
            options={"verify_aud": True},  # CHANGED: was False
        )
```

**Step 2:** Also add the web client as a valid audience. Replace the single `audience` with a list:

```python
        # Accept tokens issued for either the API or web client
        valid_audiences = [settings.KEYCLOAK_CLIENT_ID, "quicktrust-web", "account"]

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=valid_audiences,
            issuer=issuer,
            options={"verify_aud": True},
        )
```

**Verify:**
```bash
# Create a token for a different client and confirm it is rejected
pytest tests/test_rbac.py -v
```

---

### 1.3 Add Startup Validation for Default Secrets (Audit C-3)

**Why:** Deploying with `SECRET_KEY = "change-me-in-production"` is a critical vulnerability.

**File:** `backend/app/config.py`

**Step 1:** Add a validation method to the `Settings` class after line 50:

```python
# backend/app/config.py - add inside Settings class, before model_config

    from pydantic import model_validator

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        if self.APP_ENV == "production":
            insecure_defaults = {
                "SECRET_KEY": "change-me-in-production",
                "KEYCLOAK_CLIENT_SECRET": "quicktrust-api-secret",
                "MINIO_ROOT_PASSWORD": "quicktrust_dev",
            }
            for field_name, default_value in insecure_defaults.items():
                if getattr(self, field_name) == default_value:
                    raise ValueError(
                        f"CRITICAL: {field_name} still has the insecure default value. "
                        f"Set a strong, unique value in your .env file before deploying."
                    )
        return self
```

**Step 2:** Update `.env.example` with warnings:

```bash
# .env.example
# SECURITY: You MUST change ALL of these values before deploying to production.
# The application will refuse to start in production mode with default values.
SECRET_KEY=CHANGE_ME_generate_with_openssl_rand_hex_32
KEYCLOAK_CLIENT_SECRET=CHANGE_ME_match_keycloak_config
MINIO_ROOT_PASSWORD=CHANGE_ME_strong_password
```

**Verify:**
```bash
APP_ENV=production SECRET_KEY=change-me-in-production python -c "from app.config import Settings; Settings()" 2>&1 | grep "CRITICAL"
# Should show validation error
```

---

### 1.4 Add Authentication to Template Endpoints (Audit H-4)

**Why:** Control/evidence/policy templates are exposed to anonymous users.

**Files:**
- `backend/app/api/v1/control_templates.py`
- `backend/app/api/v1/evidence_templates.py`
- `backend/app/api/v1/policy_templates.py`

**Step 1:** Add auth dependency to `control_templates.py`. Change line 7 and add to every endpoint:

```python
# backend/app/api/v1/control_templates.py - line 7
from app.core.dependencies import DB, AnyInternalUser

# Line 17 - add current_user parameter
@router.get("", response_model=PaginatedResponse)
async def list_control_templates(
    db: DB,
    current_user: AnyInternalUser,  # <-- ADD THIS
    domain: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):

# Line 44 - add current_user parameter
@router.get("/{template_id}", response_model=ControlTemplateResponse)
async def get_control_template(template_id: UUID, db: DB, current_user: AnyInternalUser):
```

**Step 2:** Repeat the same pattern for `evidence_templates.py` and `policy_templates.py`.

**Verify:**
```bash
# Unauthenticated request should return 401
curl -s http://localhost:8000/api/v1/control-templates | jq .detail
# Should return: "Missing or invalid authorization header"
```

---

### 1.5 Suppress Database Error Details in Health Endpoint (Audit H-6)

**File:** `backend/app/main.py`

**Step 1:** Replace lines 55-56:

```python
# backend/app/main.py - replace lines 55-56
    except Exception:
        return {"status": "not_ready", "database": "unavailable"}
```

**Verify:**
```bash
# Stop postgres, hit health endpoint, confirm no error details leaked
curl http://localhost:8000/health/ready
```

---

### 1.6 Fix SQL Injection Pattern in Tenant Service (Audit C-1)

**File:** `backend/app/services/tenant_service.py`

**Step 1:** Replace the f-string SQL with a model-based approach. Replace lines ~128-150:

```python
# backend/app/services/tenant_service.py

from app.models import (
    Control, Evidence, Policy, Risk, Incident, Vendor,
    Integration, Audit, TrainingCourse, AgentRun
)

SCOPED_MODELS = [
    Control, Evidence, Policy, Risk, Incident, Vendor,
    Integration, Audit, TrainingCourse, AgentRun,
]

async def check_tenant_isolation(db: AsyncSession, org_id: UUID) -> dict:
    results = {}
    for model in SCOPED_MODELS:
        table_name = model.__tablename__
        # Use ORM queries instead of raw SQL
        total_q = select(func.count()).select_from(model)
        total = (await db.execute(total_q)).scalar() or 0

        scoped_q = select(func.count()).select_from(model).where(model.org_id == org_id)
        scoped = (await db.execute(scoped_q)).scalar() or 0

        results[table_name] = {"total": total, "scoped": scoped}
    return results
```

**Verify:**
```bash
pytest tests/test_tenants.py -v
```

---

## Phase 2: Core Security Hardening (Weeks 2-3)

### 2.1 Add Rate Limiting (Audit H-1)

**Step 1:** Add `slowapi` to dependencies:

```toml
# backend/pyproject.toml - add to dependencies
    "slowapi>=0.1.9",
```

**Step 2:** Create rate limiting configuration:

```python
# backend/app/core/rate_limit.py (NEW FILE)
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."},
    )
```

**Step 3:** Register in `main.py` after line 28:

```python
# backend/app/main.py - add after app creation (line 28)
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
```

**Step 4:** Apply stricter limits on sensitive endpoints:

```python
# backend/app/api/v1/auth.py - add rate limit decorator
from app.core.rate_limit import limiter

@router.post("/token")
@limiter.limit("5/minute")  # Strict limit for auth
async def login(request: Request, form_data: TokenRequest, db: DB):
    ...

# backend/app/api/v1/agent_runs.py - add rate limit
@router.post("/orgs/{org_id}/agent-runs/trigger")
@limiter.limit("10/minute")  # Limit expensive LLM calls
async def trigger_agent(request: Request, ...):
    ...
```

**Verify:**
```bash
# Hit login endpoint 6 times rapidly
for i in {1..6}; do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost:8000/api/v1/auth/token; done
# 6th request should return 429
```

---

### 2.2 Add Security Response Headers (Audit H-2)

**File:** `backend/app/main.py`

**Step 1:** Create a security headers middleware:

```python
# backend/app/core/security_headers.py (NEW FILE)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; font-src 'self' data:; "
            "connect-src 'self' https:; frame-ancestors 'none'"
        )
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        return response
```

**Step 2:** Register in `main.py` after CORS middleware (line 36):

```python
# backend/app/main.py - add after CORS middleware
from app.core.security_headers import SecurityHeadersMiddleware
app.add_middleware(SecurityHeadersMiddleware)
```

**Verify:**
```bash
curl -sI http://localhost:8000/health | grep -E "X-Content|X-Frame|Referrer|Content-Security"
```

---

### 2.3 Restrict CORS Methods and Headers (Audit H-3)

**File:** `backend/app/main.py`

**Step 1:** Replace lines 30-36:

```python
# backend/app/main.py - replace lines 30-36
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Request-ID"],
)
```

---

### 2.4 Implement Functional Logout (Audit H-5)

**File:** `backend/app/api/v1/auth.py`

**Step 1:** Replace the logout endpoint (lines 32-34):

```python
# backend/app/api/v1/auth.py - replace logout endpoint
from fastapi import Header
from app.core.dependencies import CurrentUser
import httpx

@router.post("/logout")
async def logout(
    current_user: CurrentUser,
    authorization: str = Header(...),
):
    """Revoke the access token in Keycloak and invalidate the session."""
    token = authorization.split(" ", 1)[1]
    settings = get_settings()

    revoke_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/revoke"
    )

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                revoke_url,
                data={
                    "token": token,
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "token_type_hint": "access_token",
                },
            )
        except httpx.HTTPError:
            pass  # Best effort -- token will expire naturally

    return {"message": "Token revoked successfully"}
```

**Step 2:** Add Redis-based token blacklist for defense-in-depth:

```python
# backend/app/core/token_blacklist.py (NEW FILE)
import redis.asyncio as redis
from app.config import get_settings

settings = get_settings()
_redis = None


async def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def blacklist_token(jti: str, expires_in: int):
    """Add a token's JTI to the blacklist until it naturally expires."""
    r = await get_redis()
    await r.setex(f"blacklist:{jti}", expires_in, "1")


async def is_token_blacklisted(jti: str) -> bool:
    """Check if a token has been revoked."""
    r = await get_redis()
    return await r.exists(f"blacklist:{jti}") > 0
```

**Step 3:** Add blacklist check to `security.py` after line 66:

```python
# backend/app/core/security.py - add after payload = jwt.decode(...)
        # Check token blacklist
        from app.core.token_blacklist import is_token_blacklisted
        jti = payload.get("jti")
        if jti and await is_token_blacklisted(jti):
            raise UnauthorizedError("Token has been revoked")
```

---

### 2.5 Add Evidence Upload Validation (Audit H-7)

**File:** `backend/app/api/v1/evidence.py`

**Step 1:** Add validation constants and logic before the upload handler:

```python
# backend/app/api/v1/evidence.py - add after imports

EVIDENCE_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "text/csv",
    "application/json",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}
EVIDENCE_MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
```

**Step 2:** Add validation inside the upload endpoint (before `contents = await file.read()`):

```python
    # Validate content type
    if file.content_type not in EVIDENCE_ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' is not allowed for evidence upload.",
        )

    # Read with size limit
    contents = bytearray()
    while True:
        chunk = await file.read(8192)
        if not chunk:
            break
        contents.extend(chunk)
        if len(contents) > EVIDENCE_MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum size of {EVIDENCE_MAX_FILE_SIZE // (1024*1024)}MB.",
            )
    contents = bytes(contents)
```

---

### 2.6 Add Background Task Error Handling (Audit H-8)

**Step 1:** Create a safe task runner utility:

```python
# backend/app/core/task_runner.py (NEW FILE)
import asyncio
import logging
from typing import Callable, Coroutine, Any
from uuid import UUID

from app.core.database import async_session
from app.models.agent_run import AgentRun

logger = logging.getLogger(__name__)

# Track active tasks per org for concurrency control
_active_tasks: dict[str, int] = {}
MAX_CONCURRENT_TASKS_PER_ORG = 5


async def run_safe_task(
    coro: Coroutine,
    agent_run_id: UUID | None = None,
    org_id: UUID | None = None,
):
    """Run an async task with error handling, logging, and concurrency limits."""
    org_key = str(org_id) if org_id else "global"

    # Check concurrency limit
    if _active_tasks.get(org_key, 0) >= MAX_CONCURRENT_TASKS_PER_ORG:
        logger.warning(f"Concurrency limit reached for org {org_key}")
        if agent_run_id:
            await _mark_agent_run_failed(agent_run_id, "Concurrency limit exceeded")
        return

    _active_tasks[org_key] = _active_tasks.get(org_key, 0) + 1
    try:
        await coro
    except Exception as e:
        logger.error(f"Background task failed: {e}", exc_info=True)
        if agent_run_id:
            await _mark_agent_run_failed(agent_run_id, str(e))
    finally:
        _active_tasks[org_key] = max(0, _active_tasks.get(org_key, 0) - 1)


async def _mark_agent_run_failed(agent_run_id: UUID, error: str):
    try:
        async with async_session() as db:
            from sqlalchemy import select
            result = await db.execute(
                select(AgentRun).where(AgentRun.id == agent_run_id)
            )
            run = result.scalar_one_or_none()
            if run:
                run.status = "failed"
                run.error_message = error[:2000]
                await db.commit()
    except Exception as e:
        logger.error(f"Failed to mark agent run as failed: {e}")


def create_safe_task(
    coro: Coroutine,
    agent_run_id: UUID | None = None,
    org_id: UUID | None = None,
):
    """Create a background task with proper error handling."""
    task = asyncio.create_task(run_safe_task(coro, agent_run_id, org_id))
    task.add_done_callback(lambda t: t.result() if not t.cancelled() and not t.exception() else None)
    return task
```

**Step 2:** Replace `asyncio.create_task()` calls across the codebase:

```python
# backend/app/api/v1/agent_runs.py - replace asyncio.create_task at ~line 37
from app.core.task_runner import create_safe_task

# Old:
# asyncio.create_task(_run_agent(str(agent_run.id), str(org_id)))

# New:
create_safe_task(
    _run_agent(str(agent_run.id), str(org_id)),
    agent_run_id=agent_run.id,
    org_id=org_id,
)
```

Repeat for `onboarding.py` and any other `asyncio.create_task()` usage.

---

### 2.7 Sanitize Prowler CLI Arguments (Audit H-9)

**File:** `backend/app/collectors/prowler_collectors.py`

**Step 1:** Add an allowlist and validation:

```python
# backend/app/collectors/prowler_collectors.py - add before collect()

import re

ALLOWED_SERVICES = {
    "accessanalyzer", "account", "acm", "apigateway", "autoscaling",
    "cloudformation", "cloudfront", "cloudtrail", "cloudwatch", "config",
    "dynamodb", "ec2", "ecr", "ecs", "eks", "elasticache", "elb", "emr",
    "guardduty", "iam", "inspector2", "kms", "lambda", "opensearch",
    "organizations", "rds", "redshift", "route53", "s3", "sagemaker",
    "secretsmanager", "securityhub", "ses", "sns", "sqs", "ssm",
    "trustedadvisor", "vpc", "wafv2",
}

ALLOWED_FRAMEWORKS = {
    "aws_audit_manager_control_tower_guardrails",
    "cis_1.4_aws", "cis_1.5_aws", "cis_2.0_aws", "cis_3.0_aws",
    "soc2_aws", "pci_3.2.1_aws", "hipaa_aws", "iso27001_aws",
    "nist_800_53_revision_5_aws", "nist_csf_1.1_aws",
    "gdpr_aws", "fedramp_moderate_revision_4_aws",
}

SAFE_PATTERN = re.compile(r"^[a-zA-Z0-9_.\-]+$")


def validate_prowler_args(services: list[str] | None, framework: str | None):
    if services:
        for s in services:
            if s.lower() not in ALLOWED_SERVICES or not SAFE_PATTERN.match(s):
                raise ValueError(f"Invalid Prowler service: {s}")
    if framework:
        if framework.lower() not in ALLOWED_FRAMEWORKS or not SAFE_PATTERN.match(framework):
            raise ValueError(f"Invalid Prowler framework: {framework}")
```

**Step 2:** Call validation before building the command:

```python
    # Inside collect() method, before building cmd:
    validate_prowler_args(
        scan_scope.get("services") if scan_scope else None,
        scan_scope.get("compliance_framework") if scan_scope else None,
    )
```

---

### 2.8 Add JWKS Cache TTL (Audit M-6)

**File:** `backend/app/core/security.py`

**Step 1:** Replace the global cache with a TTL-based approach:

```python
# backend/app/core/security.py - replace lines 10-28
import time

_jwks_cache: dict | None = None
_jwks_cache_time: float = 0
JWKS_CACHE_TTL = 300  # 5 minutes


async def get_jwks() -> dict:
    global _jwks_cache, _jwks_cache_time
    if _jwks_cache is not None and (time.monotonic() - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache

    jwks_url = f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/certs"
    async with httpx.AsyncClient() as client:
        resp = await client.get(jwks_url)
        resp.raise_for_status()
        _jwks_cache = resp.json()
        _jwks_cache_time = time.monotonic()
        return _jwks_cache


def clear_jwks_cache():
    global _jwks_cache, _jwks_cache_time
    _jwks_cache = None
    _jwks_cache_time = 0
```

---

## Phase 3: Data Integrity & Schema Validation (Weeks 4-5)

### 3.1 Add Audit Trail Fields to BaseModel (Audit 4.1)

**File:** `backend/app/models/base.py`

**Step 1:** Extend `BaseModel` class (lines 70-81):

```python
# backend/app/models/base.py - replace BaseModel class
class BaseModel(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(GUID(), nullable=True)
    updated_by: Mapped[uuid.UUID | None] = mapped_column(GUID(), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
```

**Step 2:** Create Alembic migration:

```bash
cd backend
alembic revision --autogenerate -m "add_audit_trail_fields_to_base_model"
alembic upgrade head
```

**Step 3:** Add a soft-delete mixin for query filtering:

```python
# backend/app/models/base.py - add below BaseModel class
from sqlalchemy import event

def soft_delete_filter(query, model_class):
    """Apply soft-delete filter to exclude deleted records by default."""
    return query.where(model_class.deleted_at.is_(None))
```

**Step 4:** Update all service layers to set `created_by`/`updated_by` when creating/updating records. Example for controls:

```python
# backend/app/services/control_service.py - in create_control()
control = Control(
    **data.model_dump(),
    org_id=org_id,
    created_by=current_user_id,  # Pass user ID from the endpoint
)
```

---

### 3.2 Add Database Indexes (Audit 4.3)

**Step 1:** Create a dedicated Alembic migration:

```bash
cd backend
alembic revision -m "add_performance_indexes"
```

**Step 2:** Populate the migration:

```python
# backend/alembic/versions/xxxx_add_performance_indexes.py
from alembic import op

def upgrade():
    # Core tenant-scoping indexes
    op.create_index("ix_controls_org_id", "controls", ["org_id"])
    op.create_index("ix_controls_status", "controls", ["status"])
    op.create_index("ix_controls_owner_id", "controls", ["owner_id"])
    op.create_index("ix_evidence_org_id_control_id", "evidence", ["org_id", "control_id"])
    op.create_index("ix_evidence_status", "evidence", ["status"])
    op.create_index("ix_evidence_expires_at", "evidence", ["expires_at"])
    op.create_index("ix_risks_org_id_risk_level", "risks", ["org_id", "risk_level"])
    op.create_index("ix_policies_org_id_status", "policies", ["org_id", "status"])
    op.create_index("ix_incidents_org_id_status_severity", "incidents", ["org_id", "status", "severity"])
    op.create_index("ix_vendors_org_id_risk_tier", "vendors", ["org_id", "risk_tier"])
    op.create_index("ix_audit_logs_org_id_timestamp", "audit_logs", ["org_id", "timestamp"])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_type", "entity_id"])
    op.create_index("ix_notifications_user_read", "notifications", ["user_id", "is_read"])
    op.create_index("ix_agent_runs_org_id_status", "agent_runs", ["org_id", "status"])
    op.create_index("ix_training_assignments_user_status", "training_assignments", ["user_id", "status"])
    op.create_index("ix_access_review_entries_campaign", "access_review_entries", ["campaign_id", "decision"])
    op.create_index("ix_monitor_alerts_org_status", "monitor_alerts", ["org_id", "status"])
    # Soft-delete filter index
    op.create_index("ix_controls_not_deleted", "controls", ["deleted_at"], postgresql_where="deleted_at IS NULL")

def downgrade():
    # Drop all indexes created above
    op.drop_index("ix_controls_org_id")
    op.drop_index("ix_controls_status")
    op.drop_index("ix_controls_owner_id")
    op.drop_index("ix_evidence_org_id_control_id")
    op.drop_index("ix_evidence_status")
    op.drop_index("ix_evidence_expires_at")
    op.drop_index("ix_risks_org_id_risk_level")
    op.drop_index("ix_policies_org_id_status")
    op.drop_index("ix_incidents_org_id_status_severity")
    op.drop_index("ix_vendors_org_id_risk_tier")
    op.drop_index("ix_audit_logs_org_id_timestamp")
    op.drop_index("ix_audit_logs_entity")
    op.drop_index("ix_notifications_user_read")
    op.drop_index("ix_agent_runs_org_id_status")
    op.drop_index("ix_training_assignments_user_status")
    op.drop_index("ix_access_review_entries_campaign")
    op.drop_index("ix_monitor_alerts_org_status")
    op.drop_index("ix_controls_not_deleted")
```

**Verify:**
```bash
alembic upgrade head
# Check indexes exist
psql -U quicktrust -c "\di" quicktrust
```

---

### 3.3 Add Unique Constraints (Audit 4.4)

**Step 1:** Create migration:

```python
# In the same or separate migration file
def upgrade():
    op.create_unique_constraint(
        "uq_control_framework_mapping",
        "control_framework_mappings",
        ["control_id", "framework_id", "requirement_id"],
    )
    op.create_unique_constraint(
        "uq_risk_control_mapping",
        "risk_control_mappings",
        ["risk_id", "control_id"],
    )
    op.create_unique_constraint(
        "uq_training_assignment",
        "training_assignments",
        ["course_id", "user_id"],
    )
    op.create_unique_constraint(
        "uq_framework_domain_code",
        "framework_domains",
        ["framework_id", "code"],
    )
    op.create_unique_constraint(
        "uq_framework_requirement_code",
        "framework_requirements",
        ["domain_id", "code"],
    )
    op.create_unique_constraint(
        "uq_control_template_evidence_template",
        "control_template_evidence_templates",
        ["control_template_id", "evidence_template_id"],
    )
```

---

### 3.4 Add Check Constraints (Audit 4.5)

```python
# Same migration file - add check constraints
def upgrade():
    op.create_check_constraint("ck_risks_likelihood", "risks", "likelihood BETWEEN 1 AND 5")
    op.create_check_constraint("ck_risks_impact", "risks", "impact BETWEEN 1 AND 5")
    op.create_check_constraint("ck_risks_risk_score", "risks", "risk_score BETWEEN 1 AND 25")
    op.create_check_constraint(
        "ck_risks_risk_level", "risks",
        "risk_level IN ('low', 'medium', 'high', 'critical')"
    )
    op.create_check_constraint(
        "ck_controls_status", "controls",
        "status IN ('draft', 'in_progress', 'implemented', 'not_implemented', 'not_applicable')"
    )
    op.create_check_constraint(
        "ck_controls_effectiveness", "controls",
        "effectiveness IN ('effective', 'partially_effective', 'not_effective', 'not_assessed')"
    )
    op.create_check_constraint(
        "ck_incidents_severity", "incidents",
        "severity IN ('P1', 'P2', 'P3', 'P4')"
    )
    op.create_check_constraint(
        "ck_vendors_risk_tier", "vendors",
        "risk_tier IN ('critical', 'high', 'medium', 'low')"
    )
    op.create_check_constraint(
        "ck_auditor_profiles_rating", "auditor_profiles",
        "rating BETWEEN 0 AND 5"
    )
```

---

### 3.5 Add Enum Validation to All Schemas (Audit 4.9)

**Step 1:** Create a shared enums module:

```python
# backend/app/schemas/enums.py (NEW FILE)
from enum import StrEnum


class ControlStatus(StrEnum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    NOT_IMPLEMENTED = "not_implemented"
    NOT_APPLICABLE = "not_applicable"


class ControlEffectiveness(StrEnum):
    EFFECTIVE = "effective"
    PARTIALLY_EFFECTIVE = "partially_effective"
    NOT_EFFECTIVE = "not_effective"
    NOT_ASSESSED = "not_assessed"


class AutomationLevel(StrEnum):
    MANUAL = "manual"
    SEMI_AUTOMATED = "semi_automated"
    AUTOMATED = "automated"


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(StrEnum):
    OPERATIONAL = "operational"
    COMPLIANCE = "compliance"
    SECURITY = "security"
    FINANCIAL = "financial"


class RiskTreatment(StrEnum):
    MITIGATE = "mitigate"
    ACCEPT = "accept"
    TRANSFER = "transfer"
    AVOID = "avoid"


class EvidenceStatus(StrEnum):
    PENDING = "pending"
    COLLECTED = "collected"
    APPROVED = "approved"
    EXPIRED = "expired"
    REJECTED = "rejected"


class IncidentSeverity(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class VendorRiskTier(StrEnum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PolicyStatus(StrEnum):
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AuditType(StrEnum):
    EXTERNAL = "external"
    INTERNAL = "internal"


class ReportFormat(StrEnum):
    PDF = "pdf"
    CSV = "csv"
    JSON = "json"


class UserRole(StrEnum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    COMPLIANCE_MANAGER = "compliance_manager"
    CONTROL_OWNER = "control_owner"
    EMPLOYEE = "employee"
    EXECUTIVE = "executive"
    AUDITOR_INTERNAL = "auditor_internal"
    AUDITOR_EXTERNAL = "auditor_external"
```

**Step 2:** Update schemas to use enums. Example for `control.py`:

```python
# backend/app/schemas/control.py - updated
from app.schemas.enums import ControlStatus, AutomationLevel, ControlEffectiveness

class ControlCreate(BaseModel):
    template_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    implementation_details: str | None = Field(None, max_length=10000)
    owner_id: UUID | None = None
    status: ControlStatus = ControlStatus.DRAFT
    automation_level: AutomationLevel = AutomationLevel.MANUAL
    test_procedure: str | None = Field(None, max_length=5000)


class ControlUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    implementation_details: str | None = Field(None, max_length=10000)
    owner_id: UUID | None = None
    status: ControlStatus | None = None
    effectiveness: ControlEffectiveness | None = None
    automation_level: AutomationLevel | None = None
    test_procedure: str | None = Field(None, max_length=5000)
```

**Step 3:** Repeat for all other schemas (risk.py, evidence.py, incident.py, vendor.py, policy.py, audit.py, monitoring.py, etc.). Each `str` status/type field gets replaced with its corresponding enum.

**Step 4:** Fix `PaginationParams` bounds:

```python
# backend/app/schemas/common.py
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, le=10000)
    page_size: int = Field(50, ge=1, le=100)
```

**Step 5:** Fix `UserUpdate.role` validation:

```python
# backend/app/schemas/user.py
from app.schemas.enums import UserRole

class UserUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=255)
    role: UserRole | None = None
    department: str | None = Field(None, max_length=100)
    is_active: bool | None = None
```

---

### 3.6 Add Cascade Rules to Foreign Keys (Audit 4.6)

**Step 1:** Create migration to add cascade rules:

```python
# Alembic migration
def upgrade():
    # Drop and re-create FKs with CASCADE for child tables
    # controls.org_id
    op.drop_constraint("controls_org_id_fkey", "controls", type_="foreignkey")
    op.create_foreign_key(
        "controls_org_id_fkey", "controls", "organizations",
        ["org_id"], ["id"], ondelete="CASCADE"
    )
    # evidence.control_id
    op.drop_constraint("evidence_control_id_fkey", "evidence", type_="foreignkey")
    op.create_foreign_key(
        "evidence_control_id_fkey", "evidence", "controls",
        ["control_id"], ["id"], ondelete="CASCADE"
    )
    # evidence.org_id
    op.drop_constraint("evidence_org_id_fkey", "evidence", type_="foreignkey")
    op.create_foreign_key(
        "evidence_org_id_fkey", "evidence", "organizations",
        ["org_id"], ["id"], ondelete="CASCADE"
    )
    # policies.org_id
    op.drop_constraint("policies_org_id_fkey", "policies", type_="foreignkey")
    op.create_foreign_key(
        "policies_org_id_fkey", "policies", "organizations",
        ["org_id"], ["id"], ondelete="CASCADE"
    )
    # control_framework_mappings - CASCADE on control delete
    op.drop_constraint("control_framework_mappings_control_id_fkey", "control_framework_mappings", type_="foreignkey")
    op.create_foreign_key(
        "control_framework_mappings_control_id_fkey", "control_framework_mappings", "controls",
        ["control_id"], ["id"], ondelete="CASCADE"
    )
    # Fix collection_jobs.evidence_id - add missing FK
    op.create_foreign_key(
        "collection_jobs_evidence_id_fkey", "collection_jobs", "evidence",
        ["evidence_id"], ["id"], ondelete="SET NULL"
    )
```

---

### 3.7 Fix N+1 Query Performance (Audit 4.7)

**File:** `backend/app/models/organization.py`

**Step 1:** Change all `lazy="selectin"` to `lazy="select"` (the default lazy loading):

```python
# backend/app/models/organization.py - change all relationships
    users = relationship("User", back_populates="organization", lazy="select")
    controls = relationship("Control", back_populates="organization", lazy="select")
    evidence = relationship("Evidence", back_populates="organization", lazy="select")
    # ... repeat for all 16 relationships
```

**Step 2:** Use explicit eager loading in service queries where needed:

```python
# backend/app/services/control_service.py - example
from sqlalchemy.orm import selectinload

async def get_control_with_relations(db, control_id):
    result = await db.execute(
        select(Control)
        .where(Control.id == control_id)
        .options(
            selectinload(Control.framework_mappings),
            selectinload(Control.evidence),
        )
    )
    return result.scalar_one_or_none()
```

---

## Phase 4: AI Agent Safety (Week 6)

### 4.1 Add AI Output Validation Schemas (Audit 5.2)

```python
# backend/app/agents/common/validation.py (NEW FILE)
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class ValidatedRisk(BaseModel):
    title: str = Field(..., min_length=5, max_length=500)
    description: str = Field(..., min_length=10, max_length=5000)
    category: Literal["operational", "compliance", "security", "financial"]
    likelihood: int = Field(..., ge=1, le=5)
    impact: int = Field(..., ge=1, le=5)
    risk_score: int = Field(..., ge=1, le=25)
    risk_level: Literal["low", "medium", "high", "critical"]
    mitigation_strategy: str = Field(..., max_length=5000)

    @field_validator("risk_score")
    @classmethod
    def validate_risk_score(cls, v, info):
        expected = info.data.get("likelihood", 1) * info.data.get("impact", 1)
        if v != expected:
            return expected  # Auto-correct
        return v


class ValidatedRemediation(BaseModel):
    control_id: str
    steps: list[str] = Field(..., min_length=1, max_length=20)
    priority: Literal["critical", "high", "medium", "low"]
    estimated_effort: str = Field(..., max_length=200)


class ValidatedAuditFinding(BaseModel):
    title: str = Field(..., min_length=5, max_length=500)
    description: str = Field(..., min_length=10, max_length=5000)
    severity: Literal["critical", "major", "minor", "observation"]
    recommendation: str = Field(..., max_length=5000)


class ValidatedVendorRisk(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    risk_tier: Literal["critical", "high", "medium", "low"]
    risk_areas: list[dict] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
```

**Step 2:** Use validation in agent nodes. Example for risk assessment:

```python
# backend/app/agents/risk_assessment/nodes.py - in save_to_db
from app.agents.common.validation import ValidatedRisk
from pydantic import ValidationError

async def save_to_db(state: dict, db: AsyncSession) -> dict:
    risks = state.get("risks", [])
    validated_risks = []
    validation_errors = []

    for risk_data in risks:
        try:
            validated = ValidatedRisk(**risk_data)
            validated_risks.append(validated)
        except ValidationError as e:
            validation_errors.append({
                "input": risk_data.get("title", "unknown"),
                "errors": str(e),
            })

    # Only save validated risks
    for vr in validated_risks:
        risk = Risk(
            org_id=state["org_id"],
            title=vr.title,
            description=vr.description,
            category=vr.category,
            likelihood=vr.likelihood,
            impact=vr.impact,
            risk_score=vr.risk_score,
            risk_level=vr.risk_level,
            status="identified",
            created_by=state.get("triggered_by"),
        )
        db.add(risk)

    await db.commit()
    return {
        "saved_count": len(validated_risks),
        "validation_errors": validation_errors,
    }
```

---

### 4.2 Add Human-in-the-Loop Approval Workflow (Audit 5.3)

**Step 1:** Add `approval_status` field to `AgentRun` model:

```python
# backend/app/models/agent_run.py - add field
    approval_status: Mapped[str] = mapped_column(
        String(50), default="pending_review"
    )  # pending_review, approved, rejected
    approved_by: Mapped[uuid.UUID | None] = mapped_column(GUID())
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
```

**Step 2:** Modify agent save functions to store results as "pending" instead of auto-committing:

```python
# In all agent save_to_db functions, change from:
#   risk = Risk(...); db.add(risk); db.commit()
# To:
#   Store proposed changes in AgentRun.output_data
#   Only create actual records when approval_status changes to "approved"

async def save_to_db(state: dict, db: AsyncSession) -> dict:
    # Store proposed data in agent run output, don't create records yet
    agent_run = await db.get(AgentRun, state["agent_run_id"])
    agent_run.output_data = {
        "proposed_risks": [vr.model_dump() for vr in validated_risks],
        "validation_errors": validation_errors,
    }
    agent_run.status = "completed"
    agent_run.approval_status = "pending_review"
    await db.commit()
    return {"status": "pending_review"}
```

**Step 3:** Create an approval endpoint:

```python
# backend/app/api/v1/agent_runs.py - add new endpoint

@router.post("/orgs/{org_id}/agent-runs/{run_id}/approve")
async def approve_agent_run(
    org_id: VerifiedOrgId,
    run_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    """Approve AI-generated outputs and commit them to the database."""
    run = await agent_run_service.get_run(db, org_id, run_id)
    if not run:
        raise NotFoundError("Agent run not found")
    if run.approval_status != "pending_review":
        raise HTTPException(400, "Agent run is not pending review")

    # Apply the proposed changes based on agent_type
    await agent_run_service.apply_approved_output(db, run, current_user.id)

    run.approval_status = "approved"
    run.approved_by = current_user.id
    run.approved_at = datetime.utcnow()
    await db.commit()
    return {"status": "approved", "agent_run_id": run.id}


@router.post("/orgs/{org_id}/agent-runs/{run_id}/reject")
async def reject_agent_run(
    org_id: VerifiedOrgId,
    run_id: UUID,
    reason: str,
    db: DB,
    current_user: ComplianceUser,
):
    run = await agent_run_service.get_run(db, org_id, run_id)
    if not run:
        raise NotFoundError("Agent run not found")
    run.approval_status = "rejected"
    run.error_message = f"Rejected by {current_user.full_name}: {reason}"
    await db.commit()
    return {"status": "rejected"}
```

---

### 4.3 Add Token Budget Tracking (Audit 5.4)

**File:** `backend/app/agents/common/llm.py`

**Step 1:** Track token usage in the LLM wrapper:

```python
# backend/app/agents/common/llm.py - replace call_llm function
async def call_llm(
    messages: list[dict],
    model: str | None = None,
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> tuple[str, dict]:
    """Returns (content, usage_info)."""
    model = model or settings.LITELLM_MODEL
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            num_retries=2,
        )
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
            "model": model,
        }
        return response.choices[0].message.content, usage
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {str(e)}") from e
```

**Step 2:** Accumulate usage in agent nodes and persist to AgentRun:

```python
# In each agent's node functions, accumulate usage:
state["total_tokens"] = state.get("total_tokens", 0) + usage["total_tokens"]

# In the final save step:
agent_run.tokens_used = state.get("total_tokens", 0)
```

---

### 4.4 Add Prompt Injection Sanitization (Audit 5.1)

```python
# backend/app/agents/common/sanitize.py (NEW FILE)
import re


def sanitize_for_prompt(text: str, max_length: int = 2000) -> str:
    """Sanitize user input before inserting into LLM prompts."""
    if not text:
        return ""
    # Truncate to max length
    text = text[:max_length]
    # Remove common prompt injection patterns
    injection_patterns = [
        r"ignore\s+(all\s+)?previous\s+instructions",
        r"disregard\s+(all\s+)?above",
        r"system\s*:\s*",
        r"<\|im_start\|>",
        r"<\|im_end\|>",
        r"\[INST\]",
        r"\[/INST\]",
    ]
    for pattern in injection_patterns:
        text = re.sub(pattern, "[FILTERED]", text, flags=re.IGNORECASE)
    return text


def wrap_user_data(data: str, label: str = "USER_DATA") -> str:
    """Wrap user data in delimiters to separate it from instructions."""
    return f"<{label}>\n{sanitize_for_prompt(data)}\n</{label}>"
```

**Step 2:** Use in agent prompts:

```python
# backend/app/agents/risk_assessment/nodes.py - modify prompt construction
from app.agents.common.sanitize import sanitize_for_prompt, wrap_user_data

# Instead of:
#   prompt = IDENTIFY_RISKS_PROMPT.format(controls_json=json.dumps(controls))
# Use:
    sanitized_controls = [
        {
            "id": c["id"],
            "title": sanitize_for_prompt(c.get("title", ""), 200),
            "description": sanitize_for_prompt(c.get("description", ""), 500),
            "status": c.get("status", ""),
        }
        for c in controls
    ]
    prompt = IDENTIFY_RISKS_PROMPT.format(
        controls_json=wrap_user_data(json.dumps(sanitized_controls, indent=2), "CONTROLS")
    )
```

---

### 4.5 Flag Mock Data from Collectors (Audit 5.5, Evidence 6.3)

**Step 1:** Add `data_source` field to Evidence model:

```python
# backend/app/models/evidence.py - add field after collector
    data_source: Mapped[str] = mapped_column(
        String(20), default="live"
    )  # "live", "mock", "fallback"
```

**Step 2:** Update all collectors to return data_source in response:

```python
# backend/app/collectors/github_collectors.py - modify _mock_response
    def _mock_response(self) -> dict:
        return {
            "status": "success",
            "data_source": "mock",  # ADD THIS
            "warning": "Using mock data - real collection failed",
            # ... rest of mock data
        }

    async def collect(self, ...):
        try:
            # ... real collection logic
            return {"status": "success", "data_source": "live", ...}
        except Exception as exc:
            logger.warning(...)
            return self._mock_response()
```

**Step 3:** Update collection service to persist `data_source`:

```python
# In collection service, when creating Evidence records:
evidence.data_source = result.get("data_source", "live")
```

---

## Phase 5: Evidence & Compliance (Week 7)

### 5.1 Add Evidence Chain of Custody (Audit 6.1)

**File:** `backend/app/models/evidence.py`

**Step 1:** Add chain-of-custody fields:

```python
# backend/app/models/evidence.py - add after existing fields (line 32)
    collected_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejected_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )
    rejected_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    rejection_reason: Mapped[str | None] = mapped_column(String(1000))
    data_source: Mapped[str] = mapped_column(String(20), default="live")
```

**Step 2:** Create approval/rejection endpoints:

```python
# backend/app/api/v1/evidence.py - add new endpoints

@router.post("/{evidence_id}/approve")
async def approve_evidence(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)
    if evidence.status != "collected":
        raise HTTPException(400, "Evidence must be in 'collected' status to approve")
    evidence.status = "approved"
    evidence.approved_by = current_user.id
    evidence.approved_at = datetime.utcnow()
    await db.commit()
    await audit_service.log(db, org_id, current_user.id, "evidence.approved", evidence_id)
    return evidence


@router.post("/{evidence_id}/reject")
async def reject_evidence(
    org_id: VerifiedOrgId,
    evidence_id: UUID,
    reason: str,
    db: DB,
    current_user: ComplianceUser,
):
    evidence = await evidence_service.get_evidence(db, org_id, evidence_id)
    evidence.status = "rejected"
    evidence.rejected_by = current_user.id
    evidence.rejected_at = datetime.utcnow()
    evidence.rejection_reason = reason
    await db.commit()
    return evidence
```

---

### 5.2 Implement Evidence SHA-256 Hashing (Audit 6.2)

```python
# backend/app/core/hashing.py (NEW FILE)
import hashlib


def compute_sha256(data: bytes) -> str:
    """Compute SHA-256 hash of data and return as hex string with algorithm prefix."""
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def verify_hash(data: bytes, expected_hash: str) -> bool:
    """Verify data integrity against stored hash."""
    if not expected_hash:
        return False
    actual = compute_sha256(data)
    return actual == expected_hash
```

**Step 2:** Use in evidence upload:

```python
# backend/app/api/v1/evidence.py - in upload endpoint, after reading contents
from app.core.hashing import compute_sha256

    # Compute hash for integrity verification
    evidence.artifact_hash = compute_sha256(contents)
```

**Step 3:** Use in collectors:

```python
# backend/app/collectors/github_collectors.py - in collect methods
import json
from app.core.hashing import compute_sha256

    data_bytes = json.dumps(result_data, sort_keys=True).encode()
    return {
        "status": "success",
        "data_source": "live",
        "artifact_hash": compute_sha256(data_bytes),
        "data": result_data,
    }
```

---

### 5.3 Add Cross-Framework Mapping (Audit 7.1)

**Step 1:** Create the mapping model:

```python
# backend/app/models/cross_framework_mapping.py (NEW FILE)
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel, GUID


class CrossFrameworkMapping(BaseModel):
    __tablename__ = "cross_framework_mappings"

    requirement_a_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("framework_requirements.id"), nullable=False
    )
    requirement_b_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("framework_requirements.id"), nullable=False
    )
    mapping_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # "equivalent", "partial", "related"
    notes: Mapped[str | None] = mapped_column(String(1000))
```

**Step 2:** Add API endpoints for managing cross-framework mappings.

**Step 3:** Seed initial mappings for common SOC 2 <-> ISO 27001 <-> NIST equivalencies.

---

### 5.4 Add Compliance Posture Snapshots (Audit 7.5)

```python
# backend/app/models/compliance_snapshot.py (NEW FILE)
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import BaseModel, GUID, JSONType


class ComplianceSnapshot(BaseModel):
    __tablename__ = "compliance_snapshots"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    framework_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("frameworks.id"), nullable=False
    )
    snapshot_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    total_controls: Mapped[int] = mapped_column(default=0)
    implemented_controls: Mapped[int] = mapped_column(default=0)
    implementation_percentage: Mapped[float] = mapped_column(default=0.0)
    evidence_coverage_percentage: Mapped[float] = mapped_column(default=0.0)
    risk_score_avg: Mapped[float | None] = mapped_column()
    details: Mapped[dict | None] = mapped_column(JSONType())
    triggered_by: Mapped[str] = mapped_column(
        String(50), default="manual"
    )  # "manual", "scheduled", "audit_start"
```

---

## Phase 6: Infrastructure Hardening (Weeks 8-9)

### 6.1 Add Non-Root Users to Dockerfiles (Audit Infra 1.1.1)

**File:** `backend/Dockerfile`

```dockerfile
# backend/Dockerfile - updated
FROM python:3.12-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && adduser --disabled-password --gecos "" --uid 1001 appuser

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .
COPY . .

RUN chown -R appuser:appuser /app

FROM base AS development
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base AS production
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**File:** `frontend/Dockerfile`

```dockerfile
# frontend/Dockerfile - updated
FROM node:20-alpine AS base
RUN corepack enable && corepack prepare pnpm@latest --activate
RUN adduser -D -u 1001 appuser
WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml* ./
RUN pnpm install --frozen-lockfile || pnpm install

FROM base AS development
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
CMD ["pnpm", "dev"]

FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN pnpm build

FROM base AS production
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
RUN chown -R appuser:appuser /app
USER appuser
CMD ["pnpm", "start"]
```

---

### 6.2 Add Docker Network Segmentation (Audit Infra 1.1.3, 1.1.4)

**File:** `docker-compose.yml`

**Step 1:** Add networks at the bottom and assign services:

```yaml
# docker-compose.yml - replace the entire file's network config

# Remove host port bindings for internal services
# Change postgres ports to:
  postgres:
    # ... existing config
    expose:
      - "5432"        # Internal only, was ports: "5432:5432"
    networks:
      - backend

  redis:
    # ... existing config
    expose:
      - "6379"        # Internal only
    command: redis-server --requirepass ${REDIS_PASSWORD:-quicktrust_redis_dev}
    networks:
      - backend

  minio:
    # ... existing config
    expose:
      - "9000"        # Internal only
    ports:
      - "9001:9001"   # Console only for dev
    networks:
      - backend

  keycloak:
    # ... existing config
    ports:
      - "8080:8080"   # Needed for browser auth flow
    networks:
      - backend
      - frontend

  api:
    # ... existing config
    ports:
      - "8000:8000"
    networks:
      - backend
      - frontend

  web:
    # ... existing config
    ports:
      - "3000:3000"
    networks:
      - frontend

  traefik:
    # ... existing config
    # REMOVE --api.insecure=true
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
    networks:
      - frontend

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge
```

---

### 6.3 Add TLS/HTTPS via Traefik (Audit Infra 1.4.1)

**File:** `infra/traefik/traefik.yml`

```yaml
# infra/traefik/traefik.yml - replace entire file
api:
  dashboard: true

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@quicktrust.dev
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    exposedByDefault: false
    endpoint: "unix:///var/run/docker.sock"

log:
  level: INFO
```

**Step 2:** Add Let's Encrypt volume and labels in docker-compose.yml:

```yaml
  traefik:
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./infra/traefik/traefik.yml:/etc/traefik/traefik.yml
      - letsencrypt:/letsencrypt

  api:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.quicktrust.dev`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"

volumes:
  letsencrypt:
```

---

### 6.4 Fix Keycloak Security (Audit Infra 1.3)

**File:** `infra/keycloak/realm-export.json`

```json
// Change line 4:
"sslRequired": "external",  // was "none"
```

**File:** `docker-compose.yml` - Keycloak service:

```yaml
  keycloak:
    image: quay.io/keycloak/keycloak:26.0
    command: start --import-realm --optimized  # was start-dev
    environment:
      KC_HOSTNAME: ${KC_HOSTNAME:-localhost}
      KC_PROXY: edge
      # ... rest of env vars
```

---

### 6.5 Add Redis Authentication (Audit Infra 1.6)

**File:** `docker-compose.yml`

```yaml
  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD:-quicktrust_redis_dev}
    # ...
```

**File:** `backend/app/config.py` - update default:

```python
    REDIS_URL: str = "redis://:quicktrust_redis_dev@localhost:6379/0"
```

---

### 6.6 Add Database Backup Automation

```bash
# infra/scripts/backup.sh (NEW FILE)
#!/bin/bash
set -euo pipefail

BACKUP_DIR="/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="quicktrust_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

# Dump and compress
PGPASSWORD="${POSTGRES_PASSWORD}" pg_dump \
  -h postgres \
  -U "${POSTGRES_USER}" \
  -d "${POSTGRES_DB}" \
  --format=custom \
  | gzip > "${BACKUP_DIR}/${FILENAME}"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete

echo "Backup completed: ${FILENAME}"
```

Add to docker-compose as a cron-based service or use the API scheduler.

---

## Phase 7: Frontend Security & UX (Weeks 10-11)

### 7.1 Add Authentication Guards (Audit Frontend 2.1)

```typescript
// frontend/src/middleware.ts (NEW FILE)
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const PUBLIC_PATHS = ["/", "/login", "/trust"];
const AUDITOR_PATHS = ["/portal"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public paths
  if (PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith("/trust/"))) {
    return NextResponse.next();
  }

  // Allow auditor paths
  if (AUDITOR_PATHS.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }

  // For dashboard routes, check for auth cookie/token
  // This is a basic check - the real auth happens in the AuthProvider
  const hasAuth = request.cookies.get("kc-access") || request.headers.get("authorization");
  if (!hasAuth && pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
```

---

### 7.2 Add Global Error Boundary

```typescript
// frontend/src/components/error-boundary.tsx (NEW FILE)
"use client";

import { Component, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="flex min-h-[400px] items-center justify-center">
            <div className="text-center">
              <h2 className="text-lg font-semibold">Something went wrong</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                {this.state.error?.message || "An unexpected error occurred"}
              </p>
              <button
                className="mt-4 rounded-md bg-primary px-4 py-2 text-sm text-white"
                onClick={() => this.setState({ hasError: false, error: null })}
              >
                Try Again
              </button>
            </div>
          </div>
        )
      );
    }
    return this.props.children;
  }
}
```

---

### 7.3 Add Toast Notification System

```bash
cd frontend && pnpm add sonner
```

```typescript
// frontend/src/app/(dashboard)/layout.tsx - add Toaster
import { Toaster } from "sonner";

export default function DashboardLayout({ children }) {
  return (
    <>
      {children}
      <Toaster richColors position="top-right" />
    </>
  );
}
```

Then use in mutations:

```typescript
// In any page with mutations
import { toast } from "sonner";

updateControl.mutate(data, {
  onSuccess: () => toast.success("Control updated"),
  onError: (err) => toast.error(`Failed: ${err.message}`),
});
```

---

### 7.4 Add Form Validation with Zod

```bash
cd frontend && pnpm add zod @hookform/resolvers react-hook-form
```

Example for risk creation:

```typescript
// frontend/src/lib/validations/risk.ts (NEW FILE)
import { z } from "zod";

export const riskSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  description: z.string().max(5000).optional(),
  category: z.enum(["operational", "compliance", "security", "financial"]),
  likelihood: z.number().int().min(1).max(5),
  impact: z.number().int().min(1).max(5),
  risk_level: z.enum(["low", "medium", "high", "critical"]),
  treatment_type: z.enum(["mitigate", "accept", "transfer", "avoid"]).optional(),
});

export type RiskFormData = z.infer<typeof riskSchema>;
```

---

## Phase 8: CI/CD & DevSecOps (Week 12)

### 8.1 Fix Security Scanning (Audit Infra 2.1.1)

**File:** `.github/workflows/ci.yml`

**Step 1:** Replace the security-scan job (lines 93-105):

```yaml
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Python dependency audit
      - name: Install and audit Python deps
        run: |
          cd backend
          pip install -e .
          pip install pip-audit
          pip-audit --strict  # Fails on any vulnerability

      # Frontend dependency audit
      - uses: pnpm/action-setup@v4
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - name: Audit frontend dependencies
        run: |
          cd frontend
          pnpm install --frozen-lockfile
          pnpm audit --audit-level=high  # Fail on high+ severity

      # SAST with Semgrep
      - name: Run Semgrep SAST
        uses: semgrep/semgrep-action@v1
        with:
          config: >-
            p/python
            p/javascript
            p/typescript
            p/security-audit
            p/owasp-top-ten

  container-scan:
    name: Container Vulnerability Scan
    runs-on: ubuntu-latest
    needs: docker-build
    steps:
      - uses: actions/checkout@v4
      - name: Build backend image
        run: docker build -t quicktrust-api --target production backend/
      - name: Run Trivy on backend
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: quicktrust-api
          format: table
          exit-code: 1
          severity: CRITICAL,HIGH
      - name: Build frontend image
        run: docker build -t quicktrust-web --target production frontend/
      - name: Run Trivy on frontend
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: quicktrust-web
          format: table
          exit-code: 1
          severity: CRITICAL,HIGH
```

---

### 8.2 Add Test Coverage Enforcement

**Step 1:** Add pytest-cov to dev dependencies:

```toml
# backend/pyproject.toml - add to [project.optional-dependencies] dev
    "pytest-cov>=5.0.0",
```

**Step 2:** Update CI test job:

```yaml
  backend-test:
    name: Backend Tests
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -e ".[dev]"
      - run: pytest --tb=short -q --cov=app --cov-report=term-missing --cov-fail-under=60
```

---

### 8.3 Add Frontend Testing

```bash
cd frontend && pnpm add -D vitest @testing-library/react @testing-library/jest-dom jsdom
```

Add vitest config and initial tests:

```typescript
// frontend/vitest.config.ts (NEW FILE)
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
  },
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
});
```

---

## Phase 9: Production Readiness (Weeks 13-14)

### 9.1 Create Production Docker Compose

```yaml
# docker-compose.prod.yml (NEW FILE)
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    expose:
      - "5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./infra/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 2G
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER}"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD} --maxmemory 256mb --maxmemory-policy allkeys-lru
    expose:
      - "6379"
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 512M
    networks:
      - backend

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: production
    env_file: .env.prod
    expose:
      - "8000"
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
      replicas: 2
    networks:
      - backend
      - frontend
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

  web:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    env_file: .env.prod
    expose:
      - "3000"
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 1G
    networks:
      - frontend

  traefik:
    image: traefik:v3.2
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./infra/traefik/traefik.yml:/etc/traefik/traefik.yml
      - letsencrypt:/letsencrypt
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
    networks:
      - frontend

networks:
  backend:
    driver: bridge
  frontend:
    driver: bridge

volumes:
  postgres_data:
  letsencrypt:
```

---

### 9.2 Add Deployment Pipeline to CI

```yaml
# .github/workflows/deploy.yml (NEW FILE)
name: Deploy

on:
  push:
    branches: [main]
    paths-ignore:
      - "docs/**"
      - "*.md"

jobs:
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-build, security-scan, container-scan]
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: |
          # Build and push images
          docker build -t $REGISTRY/quicktrust-api:${{ github.sha }} --target production backend/
          docker build -t $REGISTRY/quicktrust-web:${{ github.sha }} --target production frontend/
          docker push $REGISTRY/quicktrust-api:${{ github.sha }}
          docker push $REGISTRY/quicktrust-web:${{ github.sha }}
          # Deploy via SSH/kubectl/etc

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: deploy-staging
    environment: production
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to production
        run: echo "Deploy production here"
```

---

## Phase 10: Polish & Long-Term (Weeks 15+)

### 10.1 Add PostgreSQL Row-Level Security

```sql
-- infra/postgres/rls.sql (NEW FILE)
-- Enable RLS on all tenant-scoped tables
ALTER TABLE controls ENABLE ROW LEVEL SECURITY;
ALTER TABLE evidence ENABLE ROW LEVEL SECURITY;
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;
ALTER TABLE risks ENABLE ROW LEVEL SECURITY;
ALTER TABLE incidents ENABLE ROW LEVEL SECURITY;
ALTER TABLE vendors ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY tenant_isolation_controls ON controls
    USING (org_id = current_setting('app.current_org_id')::uuid);

CREATE POLICY tenant_isolation_evidence ON evidence
    USING (org_id = current_setting('app.current_org_id')::uuid);

-- Repeat for all tenant-scoped tables...

-- Set the org context in each request (called from FastAPI middleware)
-- SET LOCAL app.current_org_id = '<org-uuid>';
```

---

### 10.2 Add Request Correlation IDs

```python
# backend/app/core/request_id.py (NEW FILE)
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

---

### 10.3 Add WCAG 2.1 Accessibility Fixes

Systematic approach for all frontend forms:

```typescript
// Example pattern for all form inputs:
<div>
  <label htmlFor="risk-title" className="text-sm font-medium">
    Title <span className="text-red-500" aria-hidden="true">*</span>
  </label>
  <input
    id="risk-title"
    type="text"
    required
    aria-required="true"
    aria-describedby="risk-title-error"
    aria-invalid={!!errors.title}
    className="w-full rounded-md border bg-background p-2 text-sm"
    value={form.title}
    onChange={(e) => setForm({ ...form, title: e.target.value })}
  />
  {errors.title && (
    <p id="risk-title-error" role="alert" className="mt-1 text-xs text-red-500">
      {errors.title}
    </p>
  )}
</div>
```

Apply this pattern to every form input across all dashboard pages.

---

### 10.4 Replace LangGraph Facade with Real Implementation or Remove

Since LangGraph provides no value currently (all graphs use no-op lambdas), either:

**Option A: Remove LangGraph** (recommended if no conditional routing needed):

```python
# Remove langgraph from pyproject.toml dependencies
# Delete all graph.py files
# Keep the sequential execution pattern that already works
```

**Option B: Implement real graph routing** for agents that need conditional logic:

```python
# backend/app/agents/risk_assessment/graph.py - real implementation
from langgraph.graph import StateGraph, END

def build_graph():
    graph = StateGraph(RiskAssessmentState)
    graph.add_node("load_controls", load_controls)  # Real function
    graph.add_node("identify_risks", identify_risk_areas)
    graph.add_node("score_risks", score_risks)
    graph.add_node("validate_output", validate_output)
    graph.add_node("save_to_db", save_to_db)

    graph.add_edge("load_controls", "identify_risks")
    graph.add_edge("identify_risks", "score_risks")
    graph.add_edge("score_risks", "validate_output")

    # Conditional: only save if validation passes
    graph.add_conditional_edges(
        "validate_output",
        lambda state: "save" if not state.get("validation_errors") else "end",
        {"save": "save_to_db", "end": END},
    )
    graph.add_edge("save_to_db", END)

    graph.set_entry_point("load_controls")
    return graph.compile()
```

---

### 10.5 Add Data Retention and GDPR Right-to-Erasure

```python
# backend/app/services/data_retention_service.py (NEW FILE)
from datetime import datetime, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.evidence import Evidence


async def enforce_retention_policies(db: AsyncSession, org_id):
    """Run retention policies: expire old evidence, archive old audit logs."""
    now = datetime.utcnow()

    # Mark expired evidence
    await db.execute(
        update(Evidence)
        .where(Evidence.org_id == org_id)
        .where(Evidence.expires_at < now)
        .where(Evidence.status != "expired")
        .values(status="expired")
    )

    # Archive audit logs older than 7 years (SOC 2 requirement)
    cutoff = now - timedelta(days=365 * 7)
    # Move to archive table or mark as archived
    await db.commit()


async def gdpr_erasure(db: AsyncSession, user_id, org_id):
    """Implement GDPR Article 17 right to erasure for a specific user."""
    # Anonymize user data instead of hard delete (preserve audit integrity)
    from app.models.user import User
    user = await db.get(User, user_id)
    if user and str(user.org_id) == str(org_id):
        user.full_name = "[REDACTED]"
        user.email = f"redacted-{user.id}@deleted.local"
        user.keycloak_id = None
        user.is_active = False
        user.deleted_at = datetime.utcnow()
        await db.commit()
```

---

## Verification Checklist

After implementing all phases, verify each category:

| Category | Verification Command | Expected Result |
|----------|---------------------|-----------------|
| Dependencies | `cd backend && pip install -e . && python -c "import asyncpg"` | No errors |
| JWT Auth | `pytest tests/test_rbac.py -v` | All pass |
| Rate Limiting | Hit login 6x rapidly | 429 on 6th |
| Security Headers | `curl -sI /health \| grep X-Content` | Headers present |
| DB Indexes | `psql -c "\di" \| wc -l` | 15+ indexes |
| Schema Validation | Send `{"status": "invalid"}` to control create | 422 error |
| AI Validation | Trigger agent, check `approval_status` | `pending_review` |
| Evidence Hash | Upload file, check `artifact_hash` | sha256:... present |
| Container Security | `docker exec api whoami` | `appuser` (not root) |
| TLS | `curl -sI https://api.quicktrust.dev` | 200 with HSTS header |
| CI Security | Push with known vuln dep | Build fails |
| Frontend Auth | Visit /dashboard without login | Redirected to /login |

---

## Estimated Effort Summary

| Phase | Duration | Effort | Priority |
|-------|----------|--------|----------|
| Phase 1: Critical Security | Week 1 | 3-4 days | P0 |
| Phase 2: Core Security | Weeks 2-3 | 5-6 days | P0 |
| Phase 3: Data Integrity | Weeks 4-5 | 5-6 days | P1 |
| Phase 4: AI Safety | Week 6 | 4-5 days | P1 |
| Phase 5: Evidence & Compliance | Week 7 | 3-4 days | P1 |
| Phase 6: Infrastructure | Weeks 8-9 | 4-5 days | P1 |
| Phase 7: Frontend | Weeks 10-11 | 5-6 days | P2 |
| Phase 8: CI/CD | Week 12 | 3-4 days | P2 |
| Phase 9: Production | Weeks 13-14 | 4-5 days | P2 |
| Phase 10: Polish | Weeks 15+ | Ongoing | P3 |

**Total: ~14-16 weeks for complete remediation of all 114 audit findings.**
