"""Middleware that assigns a unique X-Request-ID to every request.

The ID is either taken from the incoming ``X-Request-ID`` header (if
provided by an upstream proxy) or generated as a UUID4.  It is stored
in a ``ContextVar`` so any code can access it, and returned in the
response headers for end-to-end tracing.
"""

from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_context import request_id_var


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Use incoming header or generate a new one
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        token = request_id_var.set(rid)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = rid
            return response
        finally:
            request_id_var.reset(token)
