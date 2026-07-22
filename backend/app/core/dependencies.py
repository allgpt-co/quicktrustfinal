from functools import wraps
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.request_context import current_org_var
from app.core.security import decode_token
from app.models.user import User


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def _authenticate_api_key(db: AsyncSession, raw_key: str) -> User:
    """Authenticate a user via an active, unexpired X-API-Key value."""
    import hashlib
    from datetime import datetime, timezone

    from app.models.api_key import ApiKey

    key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
    result = await db.execute(select(ApiKey).where(ApiKey.key_hash == key_hash))
    api_key = result.scalar_one_or_none()
    if api_key is None:
        raise UnauthorizedError("Invalid API key")
    if not api_key.is_active:
        raise UnauthorizedError("API key has been revoked")
    if api_key.expires_at and api_key.expires_at < datetime.now(timezone.utc):
        raise UnauthorizedError("API key has expired")

    api_key.last_used_at = datetime.now(timezone.utc)
    await db.flush()
    user_result = await db.execute(select(User).where(User.id == api_key.user_id))
    user = user_result.scalar_one_or_none()
    if user is None:
        raise UnauthorizedError("API key user not found")
    if not user.is_active:
        raise ForbiddenError("User account is deactivated")
    return user


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Resolve the current database user from an application JWT or API key."""
    if x_api_key:
        return await _authenticate_api_key(db, x_api_key)
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")

    payload = await decode_token(authorization.split(" ", 1)[1])
    subject = payload.get("sub")
    try:
        user_id = UUID(subject)
    except (TypeError, ValueError):
        raise UnauthorizedError("Invalid token payload") from None

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise UnauthorizedError("User account not found")
    if not user.is_active:
        raise ForbiddenError("User account is deactivated")
    return user


async def verify_org_access(
    org_id: UUID,
    current_user: User = Depends(get_current_user),
) -> UUID:
    """Verify the authenticated user belongs to the requested organization."""
    if current_user.role == SUPER_ADMIN:
        current_org_var.set(str(org_id))
        return org_id
    if str(current_user.org_id) != str(org_id):
        raise ForbiddenError("Access denied: you do not belong to this organization")
    current_org_var.set(str(org_id))
    return org_id


async def get_optional_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        return await get_current_user(authorization=authorization, db=db)
    except Exception:
        return None


def require_role(*roles: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if current_user.role not in roles:
                raise ForbiddenError(
                    f"Role '{current_user.role}' does not have access. Required: {', '.join(roles)}"
                )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

SUPER_ADMIN = "super_admin"
COMPLIANCE_MANAGER = "compliance_manager"
CONTROL_OWNER = "control_owner"
EMPLOYEE = "employee"
EXECUTIVE = "executive"
AUDITOR_INTERNAL = "auditor_internal"
AUDITOR_EXTERNAL = "auditor_external"

ALL_ROLES = (
    SUPER_ADMIN, COMPLIANCE_MANAGER, CONTROL_OWNER, EMPLOYEE, EXECUTIVE,
    AUDITOR_INTERNAL, AUDITOR_EXTERNAL,
)
INTERNAL_ROLES = (
    SUPER_ADMIN, COMPLIANCE_MANAGER, CONTROL_OWNER, EMPLOYEE, EXECUTIVE,
    AUDITOR_INTERNAL,
)


class RoleChecker:
    """Reusable FastAPI dependency that enforces database-backed RBAC."""

    def __init__(self, *allowed_roles: str) -> None:
        self.allowed_roles: set[str] = set(allowed_roles)

    async def __call__(
        self, current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role == SUPER_ADMIN:
            return current_user
        if current_user.role not in self.allowed_roles:
            raise ForbiddenError(
                f"Role '{current_user.role}' does not have access. "
                f"Required: {', '.join(sorted(self.allowed_roles))}"
            )
        return current_user


AdminUser = Annotated[User, Depends(RoleChecker(SUPER_ADMIN))]
ComplianceUser = Annotated[
    User, Depends(RoleChecker(SUPER_ADMIN, COMPLIANCE_MANAGER))
]
AnyInternalUser = Annotated[User, Depends(RoleChecker(*INTERNAL_ROLES))]
VerifiedOrgId = Annotated[UUID, Depends(verify_org_access)]
