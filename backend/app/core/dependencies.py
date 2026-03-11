import uuid
from functools import wraps
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.core.request_context import current_org_var
from app.core.security import decode_token
from app.models.user import User
from app.models.organization import Organization


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    payload = await decode_token(token)

    keycloak_id = payload.get("sub")
    if not keycloak_id:
        raise UnauthorizedError("Invalid token payload")

    result = await db.execute(select(User).where(User.keycloak_id == keycloak_id))
    user = result.scalar_one_or_none()

    if user is None:
        # Check if a user with this email already exists (e.g. Keycloak DB was reset)
        email = payload.get("email", "")
        if email:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user is not None:
                user.keycloak_id = keycloak_id
                await db.commit()
                await db.refresh(user)
                return user

        # Auto-provision user on first Keycloak login
        user_name = payload.get("name", payload.get("preferred_username", "User"))
        user_email = payload.get("email", "")

        # Check if this user was invited to an existing organization
        from app.services.invitation_service import find_pending_invitation_by_email

        invitation = await find_pending_invitation_by_email(db, user_email) if user_email else None

        if invitation:
            # Invited user — join existing org with assigned role
            org_id = invitation.org_id
            role = invitation.role
            invitation.status = "accepted"
            from datetime import datetime, timezone as tz
            invitation.accepted_at = datetime.now(tz.utc)
        else:
            # New user (no invite) — create their own org as admin
            org_name = f"{user_name}'s Organization"
            org_slug = f"org-{uuid.uuid4().hex[:8]}"
            org = Organization(
                name=org_name,
                slug=org_slug,
                industry="Technology",
                company_size="1-50",
            )
            db.add(org)
            await db.flush()
            org_id = org.id

            # First user of their own org is always super_admin
            role = "super_admin"

        user = User(
            org_id=org_id,
            keycloak_id=keycloak_id,
            email=user_email,
            full_name=user_name,
            role=role,
            is_active=True,
        )
        db.add(user)
        await db.commit()

    if not user.is_active:
        raise ForbiddenError("User account is deactivated")

    return user


async def verify_org_access(
    org_id: UUID,
    current_user: User = Depends(get_current_user),
) -> UUID:
    """Verify the authenticated user belongs to the requested organization.

    Super admins can access any organization. All other users must belong
    to the organization specified in the URL path.
    """
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


# Type aliases for dependency injection
DB = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


# ---------------------------------------------------------------------------
# Role constants
# ---------------------------------------------------------------------------
SUPER_ADMIN = "super_admin"
COMPLIANCE_MANAGER = "compliance_manager"
CONTROL_OWNER = "control_owner"
EMPLOYEE = "employee"
EXECUTIVE = "executive"
AUDITOR_INTERNAL = "auditor_internal"
AUDITOR_EXTERNAL = "auditor_external"

ALL_ROLES = (
    SUPER_ADMIN,
    COMPLIANCE_MANAGER,
    CONTROL_OWNER,
    EMPLOYEE,
    EXECUTIVE,
    AUDITOR_INTERNAL,
    AUDITOR_EXTERNAL,
)

# Internal roles (everyone except external auditors)
INTERNAL_ROLES = (
    SUPER_ADMIN,
    COMPLIANCE_MANAGER,
    CONTROL_OWNER,
    EMPLOYEE,
    EXECUTIVE,
    AUDITOR_INTERNAL,
)


# ---------------------------------------------------------------------------
# RoleChecker – reusable FastAPI dependency
# ---------------------------------------------------------------------------
class RoleChecker:
    """FastAPI dependency that enforces role-based access control.

    Usage as a dependency:
        @router.get("/admin-only", dependencies=[Depends(RoleChecker(SUPER_ADMIN))])

    Or via Annotated type alias:
        async def endpoint(user: AdminUser): ...
    """

    def __init__(self, *allowed_roles: str) -> None:
        self.allowed_roles: set[str] = set(allowed_roles)

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
    ) -> User:
        # Super admins always pass
        if current_user.role == SUPER_ADMIN:
            return current_user

        if current_user.role not in self.allowed_roles:
            raise ForbiddenError(
                f"Role '{current_user.role}' does not have access. "
                f"Required: {', '.join(sorted(self.allowed_roles))}"
            )
        return current_user


# ---------------------------------------------------------------------------
# Convenience type aliases for common role checks
# ---------------------------------------------------------------------------
AdminUser = Annotated[User, Depends(RoleChecker(SUPER_ADMIN))]
ComplianceUser = Annotated[
    User, Depends(RoleChecker(SUPER_ADMIN, COMPLIANCE_MANAGER))
]
AnyInternalUser = Annotated[User, Depends(RoleChecker(*INTERNAL_ROLES))]

# ---------------------------------------------------------------------------
# Org-scoped access — validates the org_id path param against the user's org
# ---------------------------------------------------------------------------
VerifiedOrgId = Annotated[UUID, Depends(verify_org_access)]
