"""Request-scoped context variables for correlation IDs and tenant isolation."""

from contextvars import ContextVar

# Unique ID for each incoming HTTP request (Fix 10.2)
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

# Current org_id for RLS session variable (Fix 10.1)
current_org_var: ContextVar[str] = ContextVar("current_org", default="")
