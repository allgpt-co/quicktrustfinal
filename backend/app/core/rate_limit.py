"""Rate limiting with per-route category support.

Uses slowapi (backed by limits library) with configurable limits per
route category.  The default is 100 requests/minute per IP.

Route-specific limits are applied via the ``@limiter.limit()`` decorator:

    @router.post("/token")
    @limiter.limit(RATE_LIMITS["auth"])
    async def get_token(request: Request, ...):
        ...
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Per-route category limits (used with @limiter.limit(RATE_LIMITS["key"]))
RATE_LIMITS = {
    "auth": "5/minute",           # Login / token exchange
    "signup": "10/hour",          # Account creation
    "api": "100/minute",          # General API calls (default)
    "upload": "50/hour",          # File uploads
    "ai_query": "10/minute",      # AI agent runs, LLM calls
    "public": "30/minute",        # Public trust center, unauthenticated pages
    "admin": "30/minute",         # Admin operations
    "export": "10/hour",          # Data exports, report generation
}


async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Return 429 with Retry-After header for rate limit breaches."""
    retry_after = getattr(exc, "retry_after", 60)
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please try again later.",
        },
        headers={
            "Retry-After": str(retry_after),
        },
    )
