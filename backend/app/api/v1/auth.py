import httpx
from fastapi import APIRouter, Header, Request

from app.config import get_settings
from app.core.dependencies import CurrentUser
from app.core.rate_limit import limiter
from app.schemas.auth import TokenRequest, TokenResponse, UserInfo
from app.services.keycloak_service import keycloak_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
@limiter.limit("5/minute")
async def get_token(request: Request, req: TokenRequest):
    data = await keycloak_service.exchange_token(req.username, req.password)
    return TokenResponse(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token"),
        token_type="bearer",
        expires_in=data.get("expires_in"),
    )


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: CurrentUser):
    return UserInfo(
        keycloak_id=current_user.keycloak_id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        org_id=str(current_user.org_id),
    )


@router.post("/logout")
async def logout(
    current_user: CurrentUser,
    authorization: str = Header(...),
):
    """Revoke the access token in Keycloak and invalidate the session."""
    token = authorization.split(" ", 1)[-1]
    settings = get_settings()

    revoke_url = (
        f"{settings.KEYCLOAK_URL}/realms/{settings.KEYCLOAK_REALM}"
        f"/protocol/openid-connect/revoke"
    )

    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                revoke_url,
                data={
                    "token": token,
                    "client_id": settings.KEYCLOAK_CLIENT_ID,
                    "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
                    "token_type_hint": "access_token",
                },
            )
        except httpx.HTTPError:
            pass  # Best effort — token will expire naturally

    # Also blacklist the token's JTI in Redis for defense-in-depth
    try:
        from app.core.token_blacklist import blacklist_token
        from jose import jwt as jose_jwt

        payload = jose_jwt.get_unverified_claims(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            import time

            remaining = max(int(exp) - int(time.time()), 0)
            if remaining > 0:
                await blacklist_token(jti, remaining)
    except Exception:
        pass  # Best effort — Keycloak revocation is the primary mechanism

    return {"message": "Token revoked successfully"}
