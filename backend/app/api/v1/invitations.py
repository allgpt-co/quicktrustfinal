"""Invitation endpoints — send, list, revoke, resend, validate, and accept invitations."""

from uuid import UUID
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import (
    DB,
    ComplianceUser,
    CurrentUser,
    VerifiedOrgId,
)
from app.schemas.invitation import (
    InvitationCreate,
    InvitationResponse,
    InvitationPublicResponse,
    InvitationAcceptResponse,
)
from app.services import invitation_service

router = APIRouter(tags=["invitations"])


def _to_response(inv) -> InvitationResponse:
    """Convert Invitation model to response with flattened relationship data."""
    return InvitationResponse(
        id=inv.id,
        org_id=inv.org_id,
        invited_by=inv.invited_by,
        email=inv.email,
        role=inv.role,
        token=inv.token,
        status=inv.status,
        expires_at=inv.expires_at,
        accepted_at=inv.accepted_at,
        created_at=inv.created_at,
        updated_at=inv.updated_at,
        org_name=inv.organization.name if inv.organization else None,
        inviter_name=inv.inviter.full_name if inv.inviter else None,
    )


# ── Org-scoped endpoints (require admin) ──────────────────────────────

@router.post(
    "/organizations/{org_id}/invitations",
    response_model=InvitationResponse,
    status_code=201,
)
async def send_invitation(
    org_id: VerifiedOrgId,
    data: InvitationCreate,
    db: DB,
    current_user: ComplianceUser,
):
    """Send an invitation to a new team member."""
    inv = await invitation_service.create_invitation(
        db, org_id, data, invited_by=current_user.id
    )
    return _to_response(inv)


@router.get(
    "/organizations/{org_id}/invitations",
    response_model=dict,
)
async def list_invitations(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: ComplianceUser,
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """List all invitations for an organization."""
    items, total = await invitation_service.list_invitations(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return {
        "items": [_to_response(inv) for inv in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.delete(
    "/organizations/{org_id}/invitations/{invitation_id}",
    response_model=InvitationResponse,
)
async def revoke_invitation(
    org_id: VerifiedOrgId,
    invitation_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    """Revoke a pending invitation."""
    inv = await invitation_service.revoke_invitation(db, org_id, invitation_id)
    return _to_response(inv)


@router.post(
    "/organizations/{org_id}/invitations/{invitation_id}/resend",
    response_model=InvitationResponse,
)
async def resend_invitation(
    org_id: VerifiedOrgId,
    invitation_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    """Resend an invitation (resets expiry, generates new token)."""
    inv = await invitation_service.resend_invitation(db, org_id, invitation_id)
    return _to_response(inv)


# ── Public endpoints (no auth or user-level auth) ─────────────────────

@router.get(
    "/invitations/validate/{token}",
    response_model=InvitationPublicResponse,
)
async def validate_invitation(token: str, db: DB):
    """Validate an invitation token. Returns org name and role (public endpoint)."""
    inv = await invitation_service.validate_token(db, token)
    is_expired = inv.expires_at < datetime.now(timezone.utc) or inv.status != "pending"
    return InvitationPublicResponse(
        org_name=inv.organization.name if inv.organization else "Unknown",
        inviter_name=inv.inviter.full_name if inv.inviter else "Unknown",
        role=inv.role,
        email=inv.email,
        status=inv.status,
        expires_at=inv.expires_at,
        is_expired=is_expired,
    )


@router.post(
    "/invitations/accept/{token}",
    response_model=InvitationAcceptResponse,
)
async def accept_invitation(
    token: str,
    db: DB,
    current_user: CurrentUser,
):
    """Accept an invitation. The authenticated user joins the org with the invited role."""
    inv = await invitation_service.accept_invitation(
        db, token, current_user.email
    )

    # Update user's org and role
    current_user.org_id = inv.org_id
    current_user.role = inv.role
    await db.commit()

    return InvitationAcceptResponse(
        message=f"You have joined {inv.organization.name if inv.organization else 'the organization'} as {inv.role.replace('_', ' ').title()}",
        org_id=inv.org_id,
        role=inv.role,
    )
