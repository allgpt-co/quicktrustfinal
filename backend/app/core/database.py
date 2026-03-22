import ssl

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()


def _build_connect_args() -> dict:
    """Build SSL connect_args for asyncpg when DATABASE_SSL_CA is set."""
    if "sqlite" in settings.DATABASE_URL:
        return {}
    if not settings.DATABASE_SSL_CA:
        return {}

    # Create SSL context for asyncpg (PostgreSQL)
    ssl_ctx = ssl.create_default_context(cafile=settings.DATABASE_SSL_CA)
    ssl_ctx.check_hostname = True
    ssl_ctx.verify_mode = ssl.CERT_REQUIRED
    return {"ssl": ssl_ctx}


_connect_args = _build_connect_args()

# SQLite doesn't support pool_size/max_overflow
engine_kwargs: dict = {"echo": settings.APP_ENV == "development"}
if "sqlite" not in settings.DATABASE_URL:
    engine_kwargs["pool_size"] = 20
    engine_kwargs["max_overflow"] = 10
    if _connect_args:
        engine_kwargs["connect_args"] = _connect_args

engine = create_async_engine(settings.DATABASE_URL, **engine_kwargs)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Separate engine for background tasks (agent runs) to avoid connection pool
# conflicts with request-scoped sessions.
_bg_engine_kwargs: dict = {"echo": False}
if "sqlite" not in settings.DATABASE_URL:
    _bg_engine_kwargs["pool_size"] = 5
    _bg_engine_kwargs["max_overflow"] = 5
    if _connect_args:
        _bg_engine_kwargs["connect_args"] = _connect_args

bg_engine = create_async_engine(settings.DATABASE_URL, **_bg_engine_kwargs)
bg_async_session = async_sessionmaker(bg_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
