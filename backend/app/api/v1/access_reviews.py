from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.access_review import (
    AccessReviewCampaignCreate,
    AccessReviewCampaignUpdate,
    AccessReviewCampaignResponse,
    AccessReviewEntryCreate,
    AccessReviewEntryUpdate,
    AccessReviewEntryResponse,
    AccessReviewStatsResponse,
)
from app.services import access_review_service

router = APIRouter(
    prefix="/organizations/{org_id}/access-reviews",
    tags=["access-reviews"],
)


@router.get("", response_model=PaginatedResponse)
async def list_campaigns(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await access_review_service.list_campaigns(
        db, org_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[AccessReviewCampaignResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=AccessReviewCampaignResponse, status_code=201)
async def create_campaign(org_id: VerifiedOrgId, data: AccessReviewCampaignCreate, db: DB, current_user: ComplianceUser):
    campaign = await access_review_service.create_campaign(db, org_id, data)
    return AccessReviewCampaignResponse.model_validate({
        **{col: getattr(campaign, col) for col in campaign.__table__.columns.keys()},
        "entry_count": 0,
        "pending_count": 0,
    })


@router.get("/stats", response_model=AccessReviewStatsResponse)
async def get_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await access_review_service.get_access_review_stats(db, org_id)


# ---------------------------------------------------------------------------
# Access matrix & over-provisioned detection — STATIC ROUTES, must be above /{id}
# ---------------------------------------------------------------------------
_ROLE_ACCESS_LEVEL: dict[str, str] = {
    "super_admin": "admin",
    "compliance_manager": "write",
    "control_owner": "write",
    "executive": "read",
    "employee": "read",
    "auditor_internal": "read",
    "auditor_external": "read",
}


@router.get("/access-matrix")
async def get_access_matrix(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """Return a matrix of users × integrations with assumed access level by role."""
    from sqlalchemy import select as _select

    from app.models.integration import Integration
    from app.models.user import User

    users_result = await db.execute(_select(User).where(User.org_id == org_id))
    users = list(users_result.scalars().all())

    ints_result = await db.execute(
        _select(Integration).where(Integration.org_id == org_id)
    )
    integrations = list(ints_result.scalars().all())

    matrix: list[dict] = []
    for user in users:
        access_level = _ROLE_ACCESS_LEVEL.get(user.role, "read")
        access_list = [
            {
                "integration_id": str(integration.id),
                "integration_name": integration.name,
                "provider": integration.provider,
                "access_level": access_level,
            }
            for integration in integrations
        ]
        matrix.append(
            {
                "user_id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active,
                "access": access_list,
            }
        )

    return {
        "total_users": len(users),
        "total_integrations": len(integrations),
        "matrix": matrix,
    }


@router.get("/over-provisioned")
async def detect_over_provisioned(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser
):
    """Flag accounts whose privileges appear higher than necessary."""
    from datetime import datetime, timedelta, timezone

    from sqlalchemy import select as _select

    from app.models.user import User

    result = await db.execute(_select(User).where(User.org_id == org_id))
    users = list(result.scalars().all())

    now = datetime.now(timezone.utc)
    ninety_days_ago = now - timedelta(days=90)

    alerts: list[dict] = []
    for user in users:
        reasons: list[str] = []

        # Check for admin access with inactivity
        if user.role == "super_admin":
            last_login = getattr(user, "last_login_at", None)
            if last_login and last_login < ninety_days_ago:
                days_inactive = (now - last_login).days
                reasons.append(f"Super admin inactive for {days_inactive} days")
            elif last_login is None:
                # Field may not exist on the model — skip silently rather than flagging
                pass

        # Deactivated account still holding a privileged role
        if user.role in ("super_admin", "compliance_manager") and not user.is_active:
            reasons.append(
                f"High-privilege role ({user.role}) but account is inactive"
            )

        if reasons:
            alerts.append(
                {
                    "user_id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "reasons": reasons,
                    "recommendation": "Review and adjust access level",
                }
            )

    return {
        "total_alerts": len(alerts),
        "alerts": alerts,
    }


@router.get("/{campaign_id}", response_model=AccessReviewCampaignResponse)
async def get_campaign(org_id: VerifiedOrgId, campaign_id: UUID, db: DB, current_user: AnyInternalUser):
    return await access_review_service.get_campaign_response(db, org_id, campaign_id)


@router.patch("/{campaign_id}", response_model=AccessReviewCampaignResponse)
async def update_campaign(
    org_id: VerifiedOrgId, campaign_id: UUID, data: AccessReviewCampaignUpdate, db: DB, current_user: ComplianceUser
):
    campaign = await access_review_service.update_campaign(db, org_id, campaign_id, data)
    return await access_review_service.get_campaign_response(db, org_id, campaign_id)


@router.delete("/{campaign_id}", status_code=204)
async def delete_campaign(org_id: VerifiedOrgId, campaign_id: UUID, db: DB, current_user: ComplianceUser):
    await access_review_service.delete_campaign(db, org_id, campaign_id)


# === Entries ===

@router.get("/{campaign_id}/entries", response_model=list[AccessReviewEntryResponse])
async def list_entries(
    org_id: VerifiedOrgId, campaign_id: UUID, db: DB, current_user: AnyInternalUser,
    decision: str | None = None,
):
    return await access_review_service.list_entries(db, org_id, campaign_id, decision=decision)


@router.post("/{campaign_id}/entries", response_model=AccessReviewEntryResponse, status_code=201)
async def create_entry(
    org_id: VerifiedOrgId, campaign_id: UUID, data: AccessReviewEntryCreate, db: DB, current_user: ComplianceUser
):
    return await access_review_service.create_entry(db, org_id, campaign_id, data)


@router.patch("/{campaign_id}/entries/{entry_id}", response_model=AccessReviewEntryResponse)
async def update_entry(
    org_id: VerifiedOrgId, campaign_id: UUID, entry_id: UUID,
    data: AccessReviewEntryUpdate, db: DB, current_user: CurrentUser,
):
    return await access_review_service.update_entry(
        db, org_id, campaign_id, entry_id, data, decided_by_id=current_user.id
    )
