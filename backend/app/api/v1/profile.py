from uuid import UUID

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from app.core.dependencies import DB, CurrentUser, AdminUser, VerifiedOrgId
from app.models.user import User
from app.services.keycloak_service import keycloak_service

router = APIRouter(prefix="/profile", tags=["profile"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

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
    full_name: str | None = Field(None, max_length=255)
    department: str | None = Field(None, max_length=100)


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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _check_mfa(keycloak_id: str) -> bool:
    try:
        creds = await keycloak_service.get_user_credentials(keycloak_id)
        return any(c.get("type") == "otp" for c in creds)
    except Exception:
        return False


def _profile_dict(user: User, mfa_enabled: bool) -> dict:
    return ProfileResponse(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        department=user.department,
        org_id=str(user.org_id),
        is_active=user.is_active,
        mfa_enabled=mfa_enabled,
        created_at=user.created_at.isoformat(),
    )


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

@router.get("/me", response_model=ProfileResponse)
async def get_profile(current_user: CurrentUser, db: DB):
    mfa = await _check_mfa(current_user.keycloak_id)
    return _profile_dict(current_user, mfa)


@router.patch("/me", response_model=ProfileResponse)
async def update_profile(data: ProfileUpdate, current_user: CurrentUser, db: DB):
    if data.full_name is not None:
        current_user.full_name = data.full_name
        parts = data.full_name.split(" ", 1)
        try:
            await keycloak_service.update_user(
                current_user.keycloak_id,
                {"firstName": parts[0], "lastName": parts[1] if len(parts) > 1 else ""},
            )
        except Exception:
            pass
    if data.department is not None:
        current_user.department = data.department
    await db.commit()
    await db.refresh(current_user)
    mfa = await _check_mfa(current_user.keycloak_id)
    return _profile_dict(current_user, mfa)


# ---------------------------------------------------------------------------
# MFA
# ---------------------------------------------------------------------------

@router.get("/mfa", response_model=MfaStatusResponse)
async def get_mfa_status(current_user: CurrentUser):
    try:
        creds = await keycloak_service.get_user_credentials(current_user.keycloak_id)
        otp = next((c for c in creds if c.get("type") == "otp"), None)
        return MfaStatusResponse(
            mfa_enabled=otp is not None,
            mfa_type="totp" if otp else None,
            credential_id=otp.get("id") if otp else None,
        )
    except Exception:
        return MfaStatusResponse(mfa_enabled=False)


@router.post("/mfa/enable")
async def enable_mfa(current_user: CurrentUser):
    try:
        await keycloak_service.add_required_action(
            current_user.keycloak_id, "CONFIGURE_TOTP"
        )
        return {
            "message": "MFA setup initiated. You will be prompted to configure TOTP on your next login."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enable MFA: {e}")


@router.post("/mfa/disable")
async def disable_mfa(current_user: CurrentUser):
    try:
        creds = await keycloak_service.get_user_credentials(current_user.keycloak_id)
        otp = next((c for c in creds if c.get("type") == "otp"), None)
        if otp:
            await keycloak_service.delete_credential(
                current_user.keycloak_id, otp["id"]
            )
        await keycloak_service.remove_required_action(
            current_user.keycloak_id, "CONFIGURE_TOTP"
        )
        return {"message": "MFA disabled successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to disable MFA: {e}")


# ---------------------------------------------------------------------------
# Sessions
# ---------------------------------------------------------------------------

@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(current_user: CurrentUser):
    try:
        sessions = await keycloak_service.get_user_sessions(current_user.keycloak_id)
        return [
            SessionResponse(
                id=s.get("id", ""),
                ip_address=s.get("ipAddress"),
                started=str(s.get("start", "")),
                last_access=str(s.get("lastAccess", "")),
                clients=s.get("clients"),
            )
            for s in sessions
        ]
    except Exception:
        return []


@router.post("/sessions/logout-all")
async def logout_all_sessions(current_user: CurrentUser):
    try:
        await keycloak_service.logout_user_sessions(current_user.keycloak_id)
        return {"message": "All sessions terminated."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to terminate sessions: {e}"
        )


@router.delete("/sessions/{session_id}")
async def logout_session(session_id: str, current_user: CurrentUser):
    try:
        await keycloak_service.logout_session(session_id)
        return {"message": "Session terminated."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to terminate session: {e}"
        )


# ---------------------------------------------------------------------------
# Admin: Suspend / Reactivate
# ---------------------------------------------------------------------------

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
    await db.commit()

    try:
        await keycloak_service.set_user_enabled(target.keycloak_id, False)
        await keycloak_service.logout_user_sessions(target.keycloak_id)
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

    try:
        await keycloak_service.set_user_enabled(target.keycloak_id, True)
    except Exception:
        pass

    return {"message": f"User {target.email} reactivated."}
