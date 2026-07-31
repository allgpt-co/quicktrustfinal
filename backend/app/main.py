import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.api.v1.router import api_router
from app.core.database import engine
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.correlation import CorrelationIdMiddleware
from app.core.csrf import CSRFProtectionMiddleware
from app.core.logging_config import setup_logging
from app.core.rls import register_rls_hook

settings = get_settings()

# Configure structured logging with correlation IDs
setup_logging(settings.LOG_LEVEL)

# Register RLS session variable hook for PostgreSQL tenant isolation
register_rls_hook()


async def _create_schema_for_non_production() -> None:
    if settings.APP_ENV == "production":
        return
    if "sqlite" not in settings.DATABASE_URL:
        return

    from app.core.database import Base

    # Local development/test convenience only. Production schema changes must run through Alembic.
    import app.models  # noqa: F401 — import so all models are registered on Base.metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.scheduler import start_scheduler, stop_scheduler

    await _create_schema_for_non_production()
    await start_scheduler()
    yield
    await stop_scheduler()
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Open-source, agent-first GRC platform",
    version="0.6.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Correlation ID middleware (adds X-Request-ID to every request/response)
app.add_middleware(CorrelationIdMiddleware)

# CSRF protection (validate Origin header on state-changing requests)
app.add_middleware(CSRFProtectionMiddleware)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS — explicit methods and headers instead of wildcards
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "X-Request-ID"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok", "buildSha": os.getenv("BUILD_SHA", "unknown")}


@app.get("/health/ready")
async def health_ready():
    """Deep health check: probes database, Redis, and object storage."""
    import time
    from sqlalchemy import text
    from app.core.database import async_session

    checks = {}

    # Database probe
    t0 = time.monotonic()
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000)}
    except Exception as exc:
        checks["database"] = {"status": "unavailable", "error": str(exc)[:100]}

    # Redis probe
    t0 = time.monotonic()
    try:
        from app.core.token_blacklist import get_redis
        r = await get_redis()
        await r.ping()
        checks["redis"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000)}
    except Exception as exc:
        checks["redis"] = {"status": "unavailable", "error": str(exc)[:100]}

    # Object storage probe
    t0 = time.monotonic()
    try:
        from app.core.storage import check_storage

        ok, error = check_storage()
        if ok:
            checks["storage"] = {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000)}
        else:
            checks["storage"] = {"status": "unavailable", "error": error or "client not initialized"}
    except Exception as exc:
        checks["storage"] = {"status": "unavailable", "error": str(exc)[:100]}

    all_ok = all(c.get("status") == "ok" for c in checks.values())
    return {
        "status": "ready" if all_ok else "degraded",
        "checks": checks,
    }
