from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.dependencies import DB, CurrentUser, AdminUser, VerifiedOrgId
from app.models.auth import AuthSession
from app.models.user import User
from app.services import auth_service

router = APIRouter(prefix="/profile", tags=["profile"])


class ProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    department: str | None
    org_id: str
    is_active: bool
    mfa_enabled: bool
    created_at: str


class ProfileUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    department: str | None = Field(None, max_length=100)


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=1024)
    new_password: str = Field(..., min_length=12, max_length=1024)


class SessionResponse(BaseModel):
    id: str
    ip_address: str | None = None
    started: str | None = None
    last_access: str | None = None
    clients: dict | None = None


class MfaStatusResponse(BaseModel):
    mfa_enabled: bool
    mfa_type: str | None = None
    credential_id: str | None = None


class SuspendRequest(BaseModel):
    reason: str | None = None


def _profile_dict(user: User) -> ProfileResponse:
    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        department=user.department,
        org_id=str(user.org_id),
        is_active=user.is_active,
        mfa_enabled=False,
        created_at=user.created_at.isoformat(),
    )


@router.get("/me", response_model=ProfileResponse)
async def get_profile(current_user: CurrentUser):
    return _profile_dict(current_user)


@router.patch("/me", response_model=ProfileResponse)
async def update_profile(data: ProfileUpdate, current_user: CurrentUser, db: DB):
    if data.full_name is not None:
        current_user.full_name = data.full_name.strip()
    if data.department is not None:
        current_user.department = data.department
    await db.commit()
    await db.refresh(current_user)
    return _profile_dict(current_user)


@router.post("/password")
async def update_password(
    data: PasswordChangeRequest, current_user: CurrentUser, db: DB
):
    await auth_service.change_password(
        db, current_user, data.current_password, data.new_password
    )
    return {"message": "Password updated. Please sign in again."}


# These routes remain for API compatibility, but MFA is intentionally not part
# of the approved simple email/password authentication scope.
@router.get("/mfa", response_model=MfaStatusResponse)
async def get_mfa_status(current_user: CurrentUser):
    return MfaStatusResponse(mfa_enabled=False)


@router.post("/mfa/enable")
async def enable_mfa(current_user: CurrentUser):
    raise HTTPException(status_code=501, detail="MFA is not configured")


@router.post("/mfa/disable")
async def disable_mfa(current_user: CurrentUser):
    return {"message": "MFA is not enabled."}


@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(AuthSession)
        .where(
            AuthSession.user_id == current_user.id,
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > datetime.now(timezone.utc),
        )
        .order_by(AuthSession.last_accessed_at.desc())
    )
    return [
        SessionResponse(
            id=str(session.id),
            ip_address=session.ip_address,
            started=session.created_at.isoformat() if session.created_at else None,
            last_access=session.last_accessed_at.isoformat()
            if session.last_accessed_at
            else None,
            clients={"user_agent": session.user_agent} if session.user_agent else None,
        )
        for session in result.scalars().all()
    ]


@router.post("/sessions/logout-all")
async def logout_all_sessions(current_user: CurrentUser, db: DB):
    await auth_service.revoke_all_sessions(db, current_user.id)
    try:
        from app.core.token_blacklist import revoke_all_user_tokens
        await revoke_all_user_tokens(str(current_user.id))
    except Exception:
        pass
    return {"message": "All sessions terminated."}


@router.delete("/sessions/{session_id}")
async def logout_session(session_id: UUID, current_user: CurrentUser, db: DB):
    result = await db.execute(
        select(AuthSession).where(
            AuthSession.id == session_id,
            AuthSession.user_id == current_user.id,
            AuthSession.revoked_at.is_(None),
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    session.revoked_at = datetime.now(timezone.utc)
    await db.commit()
    return {"message": "Session terminated."}


@router.post("/organizations/{org_id}/users/{user_id}/suspend")
async def suspend_user(
    org_id: VerifiedOrgId,
    user_id: UUID,
    data: SuspendRequest,
    current_user: AdminUser,
    db: DB,
):
    result = await db.execute(
        select(User).where(User.id == user_id, User.org_id == org_id)
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    if str(target.id) == str(current_user.id):
        raise HTTPException(status_code=400, detail="Cannot suspend yourself")
    target.is_active = False
    await auth_service.revoke_all_sessions(db, target.id)
    try:
        from app.core.token_blacklist import revoke_all_user_tokens
        await revoke_all_user_tokens(str(target.id))
    except Exception:
        pass
    return {"message": f"User {target.email} suspended."}


@router.post("/organizations/{org_id}/users/{user_id}/reactivate")
async def reactivate_user(
    org_id: VerifiedOrgId,
    user_id: UUID,
    current_user: AdminUser,
    db: DB,
):
    result = await db.execute(
        select(User).where(User.id == user_id, User.org_id == org_id)
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.is_active = True
    await db.commit()
    return {"message": f"User {target.email} reactivated."}
