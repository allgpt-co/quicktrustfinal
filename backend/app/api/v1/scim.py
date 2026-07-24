"""SCIM 2.0 User Provisioning API (RFC 7644).

These endpoints are called by identity providers (Okta, Azure AD) to
automatically create, update, and deactivate users.
"""

from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session
from app.models.user import User
from app.services import auth_service, sso_service

router = APIRouter(prefix="/scim/v2", tags=["scim"])


# ---------------------------------------------------------------------------
# SCIM Auth
# ---------------------------------------------------------------------------

async def _authenticate_scim(authorization: str) -> tuple[AsyncSession, UUID]:
    """Validate SCIM bearer token and return (db_session, org_id)."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    raw_token = authorization[7:]
    db = async_session()
    org_id = await sso_service.validate_scim_token(db, raw_token)
    if not org_id:
        await db.close()
        raise HTTPException(status_code=401, detail="Invalid or expired SCIM token")
    return db, org_id


# ---------------------------------------------------------------------------
# SCIM User representation
# ---------------------------------------------------------------------------

def _user_to_scim(user: User, request_url: str = "") -> dict:
    return {
        "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
        "id": str(user.id),
        "userName": user.email,
        "displayName": user.full_name,
        "active": user.is_active,
        "name": {
            "formatted": user.full_name,
        },
        "emails": [{"value": user.email, "primary": True, "type": "work"}],
        "meta": {
            "resourceType": "User",
            "created": user.created_at.isoformat() if user.created_at else None,
        },
    }


# ---------------------------------------------------------------------------
# GET /scim/v2/Users — List users
# ---------------------------------------------------------------------------

@router.get("/Users")
async def list_users(
    request: Request,
    startIndex: int = 1,
    count: int = 100,
    filter: str | None = None,
    authorization: str = Header(...),
):
    db, org_id = await _authenticate_scim(authorization)
    try:
        q = select(User).where(User.org_id == org_id)

        # Basic SCIM filter: userName eq "email@example.com"
        if filter:
            import re
            match = re.match(r'userName\s+eq\s+"([^"]+)"', filter)
            if match:
                q = q.where(User.email == match.group(1).lower())

        result = await db.execute(q.offset(startIndex - 1).limit(min(count, 100)))
        users = list(result.scalars().all())

        from sqlalchemy import func
        total_q = select(func.count()).select_from(User).where(User.org_id == org_id)
        total = (await db.execute(total_q)).scalar() or 0

        return {
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
            "totalResults": total,
            "startIndex": startIndex,
            "itemsPerPage": len(users),
            "Resources": [_user_to_scim(u) for u in users],
        }
    finally:
        await db.close()


# ---------------------------------------------------------------------------
# POST /scim/v2/Users — Create user
# ---------------------------------------------------------------------------

@router.post("/Users", status_code=201)
async def create_user(request: Request, authorization: str = Header(...)):
    db, org_id = await _authenticate_scim(authorization)
    try:
        body = await request.json()
        email = (body.get("userName") or "").lower().strip()
        if not email:
            return _scim_error("userName (email) is required", 400)

        display_name = body.get("displayName") or ""
        if not display_name and body.get("name"):
            given = body["name"].get("givenName", "")
            family = body["name"].get("familyName", "")
            display_name = f"{given} {family}".strip()

        active = body.get("active", True)

        # Check if user already exists
        existing = await db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            return _scim_error("User already exists", 409)

        # Provision without a password; the user must use the password-reset flow.
        user = User(
            org_id=org_id,
            password_hash=None,
            email=email,
            full_name=display_name or email.split("@")[0],
            role="employee",
            is_active=active,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        await auth_service.request_password_reset(db, user.email)

        return _user_to_scim(user)
    finally:
        await db.close()


# ---------------------------------------------------------------------------
# GET /scim/v2/Users/{id} — Get single user
# ---------------------------------------------------------------------------

@router.get("/Users/{user_id}")
async def get_user(user_id: UUID, authorization: str = Header(...)):
    db, org_id = await _authenticate_scim(authorization)
    try:
        result = await db.execute(
            select(User).where(User.id == user_id, User.org_id == org_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return _scim_error("User not found", 404)
        return _user_to_scim(user)
    finally:
        await db.close()


# ---------------------------------------------------------------------------
# PATCH /scim/v2/Users/{id} — Update user
# ---------------------------------------------------------------------------

@router.patch("/Users/{user_id}")
async def update_user(user_id: UUID, request: Request, authorization: str = Header(...)):
    db, org_id = await _authenticate_scim(authorization)
    try:
        result = await db.execute(
            select(User).where(User.id == user_id, User.org_id == org_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return _scim_error("User not found", 404)

        body = await request.json()

        for op in body.get("Operations", []):
            path = op.get("path", "")
            value = op.get("value")

            # Handle active status
            if path == "active" or (isinstance(value, dict) and "active" in value):
                active = value if isinstance(value, bool) else value.get("active", True)
                user.is_active = active

                # If deactivated, revoke all sessions
                if not active:
                    try:
                        from app.core.token_blacklist import revoke_all_user_tokens
                        await revoke_all_user_tokens(str(user.id))
                    except Exception:
                        pass

            # Handle name update
            if path == "displayName" or path == "name.formatted":
                user.full_name = value if isinstance(value, str) else str(value)

        await db.commit()
        await db.refresh(user)
        return _user_to_scim(user)
    finally:
        await db.close()


# ---------------------------------------------------------------------------
# DELETE /scim/v2/Users/{id} — Remove user
# ---------------------------------------------------------------------------

@router.delete("/Users/{user_id}", status_code=204)
async def delete_user(user_id: UUID, authorization: str = Header(...)):
    db, org_id = await _authenticate_scim(authorization)
    try:
        result = await db.execute(
            select(User).where(User.id == user_id, User.org_id == org_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            return _scim_error("User not found", 404)

        # Soft-deactivate instead of hard delete
        user.is_active = False
        await db.commit()

        # Revoke sessions
        try:
            from app.core.token_blacklist import revoke_all_user_tokens
            await revoke_all_user_tokens(str(user.id))
        except Exception:
            pass
    finally:
        await db.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scim_error(detail: str, status: int):
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=status,
        content={
            "schemas": ["urn:ietf:params:scim:api:messages:2.0:Error"],
            "detail": detail,
            "status": str(status),
        },
    )
