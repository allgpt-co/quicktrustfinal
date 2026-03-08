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
from app.core.logging_config import setup_logging
from app.core.rls import register_rls_hook

settings = get_settings()

# Configure structured logging with correlation IDs
setup_logging(settings.LOG_LEVEL)

# Register RLS session variable hook for PostgreSQL tenant isolation
register_rls_hook()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.scheduler import start_scheduler, stop_scheduler

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
    return {"status": "ok"}


@app.get("/health/ready")
async def health_ready():
    from sqlalchemy import text
    from app.core.database import async_session

    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception:
        return {"status": "not_ready", "database": "unavailable"}
