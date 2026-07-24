"""Application-managed email/password authentication and refresh sessions."""

import hashlib
import html
import logging
import secrets
import smtplib
import uuid
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.core.exceptions import BadRequestError, ConflictError, UnauthorizedError
from app.core.security import (
    create_access_token,
    hash_password,
    password_needs_rehash,
    validate_password_strength,
    verify_password,
)
from app.models.auth import AuthSession, PasswordResetToken
from app.models.invitation import Invitation
from app.models.organization import Organization
from app.models.user import User

logger = logging.getLogger(__name__)
settings = get_settings()

MAX_FAILED_LOGIN_ATTEMPTS = 5
ACCOUNT_LOCK_MINUTES = 15


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _new_secret() -> str:
    return secrets.token_urlsafe(48)


def _client_metadata(request) -> tuple[str | None, str | None]:
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    return ip_address, user_agent[:500] if user_agent else None


async def _get_user_by_email(db: AsyncSession, email: str) -> User | None:
    normalized = email.strip().lower()
    result = await db.execute(
        select(User).where(func.lower(User.email) == normalized)
    )
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    """Authenticate an active local user with lockout and transparent rehashing."""
    user = await _get_user_by_email(db, email)
    now = _utcnow()

    if user and user.locked_until and _as_utc(user.locked_until) > now:
        verify_password(password, user.password_hash)
        raise UnauthorizedError("Invalid email or password")

    password_matches = verify_password(password, user.password_hash if user else None)
    if not user or not user.password_hash or not password_matches:
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
                user.locked_until = now + timedelta(minutes=ACCOUNT_LOCK_MINUTES)
                user.failed_login_attempts = 0
            await db.commit()
        raise UnauthorizedError("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError("Invalid email or password")

    user.failed_login_attempts = 0
    user.locked_until = None
    if password_needs_rehash(user.password_hash):
        user.password_hash = hash_password(password, user.email)
    await db.commit()
    await db.refresh(user)
    return user


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    full_name: str,
    password: str,
    invitation_token: str | None = None,
) -> User:
    """Create an organization owner or an invited organization member."""
    normalized_email = email.strip().lower()
    normalized_name = full_name.strip()
    if not normalized_name:
        raise BadRequestError("Full name is required")
    validate_password_strength(password, normalized_email)
    if await _get_user_by_email(db, normalized_email):
        raise ConflictError(
            "An account with this email already exists. Sign in or reset your password."
        )

    invitation: Invitation | None = None
    if invitation_token:
        result = await db.execute(
            select(Invitation).where(Invitation.token == invitation_token)
        )
        invitation = result.scalar_one_or_none()
        if not invitation or invitation.status != "pending":
            raise BadRequestError("Invalid or already-used invitation")
        if _as_utc(invitation.expires_at) <= _utcnow():
            invitation.status = "expired"
            await db.commit()
            raise BadRequestError("This invitation has expired")
        if invitation.email.strip().lower() != normalized_email:
            raise BadRequestError("This invitation was sent to a different email address")
        org_id = invitation.org_id
        role = invitation.role
        invitation.status = "accepted"
        invitation.accepted_at = _utcnow()
    else:
        org_name = f"{normalized_name}'s Organization"
        base_slug = f"org-{uuid.uuid4().hex[:8]}"
        org = Organization(
            name=org_name,
            slug=base_slug,
            industry="Technology",
            company_size="1-50",
        )
        db.add(org)
        await db.flush()
        org_id = org.id
        role = "super_admin"

    user = User(
        org_id=org_id,
        email=normalized_email,
        password_hash=hash_password(password, normalized_email),
        full_name=normalized_name,
        role=role,
        is_active=True,
        password_changed_at=_utcnow(),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def issue_session(db: AsyncSession, user: User, request) -> tuple[str, str, int]:
    """Issue an access JWT and a database-backed opaque refresh token."""
    raw_refresh_token = _new_secret()
    now = _utcnow()
    ip_address, user_agent = _client_metadata(request)
    session = AuthSession(
        user_id=user.id,
        refresh_token_hash=_token_hash(raw_refresh_token),
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        last_accessed_at=now,
    )
    access_token, expires_in = create_access_token(user)
    db.add(session)
    await db.commit()
    return access_token, raw_refresh_token, expires_in


async def rotate_session(
    db: AsyncSession, raw_refresh_token: str, request
) -> tuple[str, str, int]:
    """Rotate a refresh secret and return a new access token."""
    result = await db.execute(
        select(AuthSession).where(
            AuthSession.refresh_token_hash == _token_hash(raw_refresh_token)
        )
    )
    session = result.scalar_one_or_none()
    now = _utcnow()
    if (
        not session
        or session.revoked_at is not None
        or _as_utc(session.expires_at) <= now
    ):
        raise UnauthorizedError("Invalid or expired refresh session")

    user_result = await db.execute(select(User).where(User.id == session.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active or not user.password_hash:
        session.revoked_at = now
        await db.commit()
        raise UnauthorizedError("Invalid or expired refresh session")

    rotated_refresh_token = _new_secret()
    ip_address, user_agent = _client_metadata(request)
    session.refresh_token_hash = _token_hash(rotated_refresh_token)
    session.last_accessed_at = now
    session.ip_address = ip_address or session.ip_address
    session.user_agent = user_agent or session.user_agent
    access_token, expires_in = create_access_token(user)
    await db.commit()
    return access_token, rotated_refresh_token, expires_in


async def revoke_refresh_session(db: AsyncSession, raw_refresh_token: str | None) -> None:
    if not raw_refresh_token:
        return
    result = await db.execute(
        select(AuthSession).where(
            AuthSession.refresh_token_hash == _token_hash(raw_refresh_token)
        )
    )
    session = result.scalar_one_or_none()
    if session and session.revoked_at is None:
        session.revoked_at = _utcnow()
        await db.commit()


async def revoke_all_sessions(db: AsyncSession, user_id) -> None:
    await db.execute(
        update(AuthSession)
        .where(AuthSession.user_id == user_id, AuthSession.revoked_at.is_(None))
        .values(revoked_at=_utcnow())
    )
    await db.commit()


async def change_password(
    db: AsyncSession, user: User, current_password: str, new_password: str
) -> None:
    if not user.password_hash or not verify_password(current_password, user.password_hash):
        raise BadRequestError("Current password is incorrect")
    user.password_hash = hash_password(new_password, user.email)
    user.password_changed_at = _utcnow()
    await revoke_all_sessions(db, user.id)
    await db.commit()
    try:
        from app.core.token_blacklist import revoke_all_user_tokens

        await revoke_all_user_tokens(str(user.id))
    except Exception:
        pass


async def request_password_reset(db: AsyncSession, email: str) -> None:
    """Create and email a one-time reset token; silently ignore unknown emails."""
    user = await _get_user_by_email(db, email)
    if not user or not user.is_active:
        return

    now = _utcnow()
    await db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used_at.is_(None),
        )
        .values(used_at=now)
    )
    raw_token = _new_secret()
    reset = PasswordResetToken(
        user_id=user.id,
        token_hash=_token_hash(raw_token),
        expires_at=now + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES),
    )
    db.add(reset)
    await db.commit()
    await _send_password_reset_email(user, raw_token)


async def reset_password(db: AsyncSession, raw_token: str, new_password: str) -> None:
    result = await db.execute(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == _token_hash(raw_token)
        )
    )
    reset = result.scalar_one_or_none()
    now = _utcnow()
    if not reset or reset.used_at is not None or _as_utc(reset.expires_at) <= now:
        raise BadRequestError("Invalid or expired password reset link")

    user_result = await db.execute(select(User).where(User.id == reset.user_id))
    user = user_result.scalar_one_or_none()
    if not user or not user.is_active:
        raise BadRequestError("Invalid or expired password reset link")

    user.password_hash = hash_password(new_password, user.email)
    user.password_changed_at = now
    user.failed_login_attempts = 0
    user.locked_until = None
    reset.used_at = now
    await revoke_all_sessions(db, user.id)
    await db.commit()
    try:
        from app.core.token_blacklist import revoke_all_user_tokens

        await revoke_all_user_tokens(str(user.id))
    except Exception:
        pass


async def _send_password_reset_email(user: User, raw_token: str) -> None:
    frontend_url = settings.CORS_ORIGINS.split(",")[0].strip().rstrip("/")
    reset_url = f"{frontend_url}/reset-password?token={raw_token}"
    safe_name = html.escape(user.full_name)
    safe_url = html.escape(reset_url, quote=True)
    subject = "Set your QuickTrust password"
    html_body = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <h1 style="font-size: 24px;">QuickTrust</h1>
      <p>Hello {safe_name},</p>
      <p>Use the button below to set or reset your QuickTrust password. This link expires in {settings.PASSWORD_RESET_EXPIRE_MINUTES} minutes.</p>
      <p style="padding: 20px 0;"><a href="{safe_url}" style="background:#2563eb;color:#fff;padding:12px 24px;border-radius:6px;text-decoration:none;">Set password</a></p>
      <p>If you did not request this, you can ignore this email.</p>
      <p style="font-size:12px;color:#6b7280;">{safe_url}</p>
    </div>
    """

    if not settings.SMTP_HOST:
        logger.warning("Password reset email was not sent because SMTP_HOST is not configured: To=%s", user.email)
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = user.email
        msg.attach(MIMEText(html_body, "html"))
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        if settings.SMTP_USE_TLS:
            server.starttls()
        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_FROM_EMAIL, [user.email], msg.as_string())
        server.quit()
    except Exception as exc:
        logger.warning("Failed to send password reset email to %s: %s", user.email, exc)
