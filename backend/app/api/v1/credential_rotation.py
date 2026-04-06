"""Credential rotation status API — check which integrations need credential rotation."""

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import DB, ComplianceUser, VerifiedOrgId
from app.services.credential_rotation import check_credential_rotation

router = APIRouter(
    prefix="/organizations/{org_id}/credential-rotation",
    tags=["credential-rotation"],
)


@router.get("")
async def get_rotation_status(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
):
    """Show which integration credentials need rotation (older than 90 days)."""
    items = await check_credential_rotation(db, org_id)
    return {
        "total_checked": len(items) if not items else sum(1 for _ in items),
        "rotation_needed": len([i for i in items if i.get("status") == "rotation_needed"]),
        "threshold_days": 90,
        "integrations": items,
    }
