"""Invitation service — create, validate, accept, revoke invitations."""

import logging
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, NotFoundError
from app.models.invitation import Invitation
from app.models.user import User
from app.schemas.invitation import InvitationCreate

logger = logging.getLogger(__name__)

INVITE_EXPIRY_DAYS = 7


async def create_invitation(
    db: AsyncSession,
    org_id: UUID,
    data: InvitationCreate,
    invited_by: UUID,
) -> Invitation:
    """Create a new invitation and optionally send email."""
    # Check for existing pending invitation for this email in this org
    existing = await db.execute(
        select(Invitation).where(
            Invitation.org_id == org_id,
            Invitation.email == data.email,
            Invitation.status == "pending",
        )
    )
    if existing.scalar_one_or_none():
        raise BadRequestError(
            f"A pending invitation already exists for {data.email}. "
            "Revoke it first or resend it."
        )

    # Check if user already exists in this org
    existing_user = await db.execute(
        select(User).where(User.email == data.email, User.org_id == org_id)
    )
    if existing_user.scalar_one_or_none():
        raise BadRequestError(f"User {data.email} is already a member of this organization.")

    token = secrets.token_urlsafe(32)
    invitation = Invitation(
        org_id=org_id,
        invited_by=invited_by,
        email=data.email,
        role=data.role,
        token=token,
        status="pending",
        expires_at=datetime.now(timezone.utc) + timedelta(days=INVITE_EXPIRY_DAYS),
    )
    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    # Send invitation email (fire-and-forget)
    await _send_invitation_email(invitation)

    logger.info(
        "Invitation created: %s invited %s to org %s as %s",
        invited_by, data.email, org_id, data.role,
    )
    return invitation


async def list_invitations(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Invitation], int]:
    """List all invitations for an organization."""
    base_q = select(Invitation).where(Invitation.org_id == org_id)
    count_q = select(func.count()).select_from(Invitation).where(Invitation.org_id == org_id)

    if status:
        base_q = base_q.where(Invitation.status == status)
        count_q = count_q.where(Invitation.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = (
        base_q.offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(Invitation.created_at.desc())
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_invitation(
    db: AsyncSession, org_id: UUID, invitation_id: UUID
) -> Invitation:
    result = await db.execute(
        select(Invitation).where(
            Invitation.id == invitation_id, Invitation.org_id == org_id
        )
    )
    inv = result.scalar_one_or_none()
    if not inv:
        raise NotFoundError(f"Invitation {invitation_id} not found")
    return inv


async def validate_token(db: AsyncSession, token: str) -> Invitation:
    """Validate an invitation token. Returns the invitation if valid."""
    result = await db.execute(
        select(Invitation).where(Invitation.token == token)
    )
    invitation = result.scalar_one_or_none()
    if not invitation:
        raise NotFoundError("Invalid invitation link")
    return invitation


async def accept_invitation(
    db: AsyncSession, token: str, keycloak_id: str, user_email: str
) -> Invitation:
    """Accept an invitation — called during auto-provisioning."""
    invitation = await validate_token(db, token)

    if invitation.status != "pending":
        raise BadRequestError(f"This invitation has already been {invitation.status}")

    if invitation.expires_at < datetime.now(timezone.utc):
        invitation.status = "expired"
        await db.commit()
        raise BadRequestError("This invitation has expired. Please ask for a new one.")

    # Verify email matches
    if invitation.email.lower() != user_email.lower():
        raise BadRequestError("This invitation was sent to a different email address")

    invitation.status = "accepted"
    invitation.accepted_at = datetime.now(timezone.utc)
    await db.commit()

    logger.info(
        "Invitation accepted: %s joined org %s as %s",
        user_email, invitation.org_id, invitation.role,
    )
    return invitation


async def revoke_invitation(
    db: AsyncSession, org_id: UUID, invitation_id: UUID
) -> Invitation:
    """Revoke a pending invitation."""
    invitation = await get_invitation(db, org_id, invitation_id)
    if invitation.status != "pending":
        raise BadRequestError(f"Cannot revoke invitation with status '{invitation.status}'")

    invitation.status = "revoked"
    await db.commit()
    await db.refresh(invitation)
    logger.info("Invitation %s revoked", invitation_id)
    return invitation


async def resend_invitation(
    db: AsyncSession, org_id: UUID, invitation_id: UUID
) -> Invitation:
    """Resend an invitation — resets expiry and sends email again."""
    invitation = await get_invitation(db, org_id, invitation_id)
    if invitation.status not in ("pending", "expired"):
        raise BadRequestError(f"Cannot resend invitation with status '{invitation.status}'")

    invitation.status = "pending"
    invitation.expires_at = datetime.now(timezone.utc) + timedelta(days=INVITE_EXPIRY_DAYS)
    # Generate a new token for security
    invitation.token = secrets.token_urlsafe(32)
    await db.commit()
    await db.refresh(invitation)

    await _send_invitation_email(invitation)
    logger.info("Invitation %s resent to %s", invitation_id, invitation.email)
    return invitation


async def find_pending_invitation_by_email(
    db: AsyncSession, email: str
) -> Invitation | None:
    """Find a valid pending invitation for a given email address."""
    result = await db.execute(
        select(Invitation).where(
            Invitation.email == email,
            Invitation.status == "pending",
            Invitation.expires_at > datetime.now(timezone.utc),
        ).order_by(Invitation.created_at.desc())
    )
    return result.scalar_one_or_none()


async def _send_invitation_email(invitation: Invitation) -> None:
    """Send invitation email via SMTP. Falls back to logging when not configured."""
    from app.config import get_settings
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    settings = get_settings()

    org_name = invitation.organization.name if invitation.organization else "your organization"
    inviter_name = invitation.inviter.full_name if invitation.inviter else "A team member"
    frontend_url = settings.CORS_ORIGINS.split(",")[0].strip()
    invite_url = f"{frontend_url}/invite/{invitation.token}"

    role_display = invitation.role.replace("_", " ").title()

    subject = f"You're invited to join {org_name} on QuickTrust"
    html_body = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #e5e7eb;">
            <h1 style="color: #1f2937; font-size: 24px; margin: 0;">QuickTrust</h1>
            <p style="color: #6b7280; font-size: 14px; margin: 4px 0 0;">Compliance Platform</p>
        </div>
        <div style="padding: 32px 0;">
            <h2 style="color: #1f2937; font-size: 20px;">You've been invited!</h2>
            <p style="color: #4b5563; font-size: 16px; line-height: 1.6;">
                <strong>{inviter_name}</strong> has invited you to join
                <strong>{org_name}</strong> as a <strong>{role_display}</strong>.
            </p>
            <div style="text-align: center; padding: 24px 0;">
                <a href="{invite_url}"
                   style="display: inline-block; background-color: #2563eb; color: #ffffff;
                          padding: 12px 32px; border-radius: 8px; text-decoration: none;
                          font-size: 16px; font-weight: 600;">
                    Accept Invitation
                </a>
            </div>
            <p style="color: #6b7280; font-size: 14px;">
                This invitation expires in {INVITE_EXPIRY_DAYS} days.
                If you didn't expect this email, you can safely ignore it.
            </p>
            <p style="color: #9ca3af; font-size: 12px; margin-top: 16px;">
                Or copy this link: {invite_url}
            </p>
        </div>
        <div style="border-top: 1px solid #e5e7eb; padding-top: 16px; text-align: center;">
            <p style="color: #9ca3af; font-size: 12px;">
                Sent by QuickTrust Compliance Platform
            </p>
        </div>
    </div>
    """

    if not settings.SMTP_HOST:
        logger.info(
            "INVITATION EMAIL (SMTP not configured): To=%s, Org=%s, Role=%s, URL=%s",
            invitation.email, org_name, invitation.role, invite_url,
        )
        return

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = invitation.email
        msg.attach(MIMEText(html_body, "html"))

        if settings.SMTP_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)

        if settings.SMTP_USER:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

        server.sendmail(settings.SMTP_FROM_EMAIL, [invitation.email], msg.as_string())
        server.quit()
        logger.info("Invitation email sent to %s", invitation.email)
    except Exception as exc:
        logger.warning("Failed to send invitation email to %s: %s", invitation.email, exc)
