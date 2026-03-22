"""Lightweight audit-logging helper for API routes.

Usage in a route:
    from app.core.audit_middleware import log_audit

    @router.post(...)
    async def create_something(..., db: DB, current_user: AnyInternalUser):
        item = await service.create(db, org_id, data)
        await log_audit(db, current_user, "create", "control", str(item.id), org_id)
        return item
"""

from uuid import UUID

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.audit_log_service import log_action


def _get_client_ip(request: Request | None) -> str | None:
    if not request:
        return None
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


async def log_audit(
    db: AsyncSession,
    user: User,
    action: str,
    entity_type: str,
    entity_id: str,
    org_id: UUID | None = None,
    changes: dict | None = None,
    ip_address: str | None = None,
    request: Request | None = None,
    event_type: str | None = None,
    event_category: str = "data",
    severity: str = "INFO",
    outcome: str = "success",
) -> None:
    """Fire-and-forget audit log entry with rich context."""
    import logging

    # Auto-detect event_type from action if not provided
    if not event_type:
        action_map = {
            "create": "DATA_CREATE",
            "update": "DATA_UPDATE",
            "delete": "DATA_DELETE",
            "read": "DATA_READ",
            "export": "DATA_EXPORT",
            "login": "AUTH_LOGIN",
            "logout": "AUTH_LOGOUT",
            "enable_schedule": "ADMIN_ACTION",
            "disable_schedule": "ADMIN_ACTION",
            "suspend": "ADMIN_ACTION",
            "reactivate": "ADMIN_ACTION",
        }
        event_type = action_map.get(action, "GENERAL")

    # Auto-detect severity
    if action == "delete":
        severity = "WARN"

    ip = ip_address or _get_client_ip(request)
    user_agent = request.headers.get("user-agent") if request else None
    request_id_val = request.headers.get("x-request-id") if request else None

    try:
        await log_action(
            db=db,
            org_id=org_id or user.org_id,
            actor_id=str(user.id),
            actor_type="user",
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            event_type=event_type,
            event_category=event_category,
            severity=severity,
            outcome=outcome,
            actor_email=user.email,
            actor_role=user.role,
            actor_ip=ip,
            actor_user_agent=user_agent,
            changes=changes,
            request_id=request_id_val,
        )
    except Exception as exc:
        logging.getLogger(__name__).warning(
            "Failed to write audit log for %s %s: %s", action, entity_type, exc
        )
