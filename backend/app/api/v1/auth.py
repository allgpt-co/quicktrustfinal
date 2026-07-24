import time

from fastapi import APIRouter, Header, Request, Response
from jose import jwt as jose_jwt

from app.config import get_settings
from app.core.dependencies import CurrentUser, DB
from app.core.exceptions import UnauthorizedError
from app.core.rate_limit import RATE_LIMITS, limiter
from app.schemas.auth import (
    ForgotPasswordRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenRequest,
    TokenResponse,
    UserInfo,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()
REFRESH_COOKIE_NAME = "qt_refresh"


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite="lax",
        path="/",
        domain=settings.AUTH_COOKIE_DOMAIN or None,
    )


def _clear_refresh_cookie(response: Response) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/",
        domain=settings.AUTH_COOKIE_DOMAIN or None,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=True,
        samesite="lax",
    )


@router.post("/token", response_model=TokenResponse)
@limiter.limit(RATE_LIMITS["auth"])
async def get_token(request: Request, response: Response, req: TokenRequest, db: DB):
    user = await auth_service.authenticate_user(db, str(req.username), req.password)
    access_token, refresh_token, expires_in = await auth_service.issue_session(
        db, user, request
    )
    _set_refresh_cookie(response, refresh_token)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
    )


@router.post("/register", response_model=TokenResponse, status_code=201)
@limiter.limit(RATE_LIMITS["signup"])
async def register(request: Request, response: Response, req: RegisterRequest, db: DB):
    user = await auth_service.register_user(
        db,
        email=str(req.email),
        full_name=req.full_name,
        password=req.password,
        invitation_token=req.invitation_token,
    )
    access_token, refresh_token, expires_in = await auth_service.issue_session(
        db, user, request
    )
    _set_refresh_cookie(response, refresh_token)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in,
    )


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("30/minute")
async def refresh(request: Request, response: Response, db: DB):
    refresh_token = request.cookies.get(REFRESH_COOKIE_NAME)
    if not refresh_token:
        raise UnauthorizedError("Missing refresh session")
    access_token, rotated_token, expires_in = await auth_service.rotate_session(
        db, refresh_token, request
    )
    _set_refresh_cookie(response, rotated_token)
    return TokenResponse(
        access_token=access_token,
        refresh_token=rotated_token,
        expires_in=expires_in,
    )


@router.get("/me", response_model=UserInfo)
async def get_me(current_user: CurrentUser):
    return UserInfo(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        org_id=str(current_user.org_id),
    )


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: DB,
    authorization: str = Header(...),
):
    token = authorization.split(" ", 1)[-1]
    await auth_service.revoke_refresh_session(
        db, request.cookies.get(REFRESH_COOKIE_NAME)
    )
    _clear_refresh_cookie(response)

    try:
        from app.core.token_blacklist import blacklist_token

        payload = jose_jwt.get_unverified_claims(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti and exp:
            remaining = max(int(exp) - int(time.time()), 0)
            if remaining:
                await blacklist_token(jti, remaining)
    except Exception:
        pass

    return {"message": "Token revoked successfully"}


@router.post("/password/forgot")
@limiter.limit(RATE_LIMITS["auth"])
async def forgot_password(request: Request, req: ForgotPasswordRequest, db: DB):
    await auth_service.request_password_reset(db, str(req.email))
    return {
        "message": "If an active account exists for that email, a password link has been sent."
    }


@router.post("/password/reset")
@limiter.limit(RATE_LIMITS["auth"])
async def reset_password(request: Request, req: ResetPasswordRequest, db: DB):
    await auth_service.reset_password(db, req.token, req.new_password)
    return {"message": "Password updated successfully"}
