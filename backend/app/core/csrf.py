"""CSRF protection middleware for FastAPI.

Validates that the Origin header on state-changing requests (POST, PUT,
PATCH, DELETE) matches the allowed origins.  This prevents cross-site
request forgery without requiring CSRF tokens, since we use
an HttpOnly SameSite refresh cookie and Bearer access tokens for auth.

Skips validation for:
- GET, HEAD, OPTIONS requests (safe methods)
- Requests without an Origin header (same-origin browser requests, non-browser clients)
- Health check endpoints
"""

import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import get_settings

logger = logging.getLogger(__name__)

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
SKIP_PATHS = {"/health", "/health/ready"}


class CSRFProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method in SAFE_METHODS:
            return await call_next(request)

        if request.url.path in SKIP_PATHS:
            return await call_next(request)

        origin = request.headers.get("origin")
        if not origin:
            # No Origin header = same-origin or non-browser client (curl, etc.)
            return await call_next(request)

        settings = get_settings()
        allowed_origins = set(settings.cors_origins_list)

        if origin not in allowed_origins:
            logger.warning(
                "CSRF blocked: origin=%s not in allowed origins, path=%s",
                origin,
                request.url.path,
            )
            return JSONResponse(
                status_code=403,
                content={"detail": "CSRF validation failed: origin mismatch"},
            )

        return await call_next(request)
