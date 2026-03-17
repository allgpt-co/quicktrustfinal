"""Phase 5: Dashboard aggregation API endpoints."""

from fastapi import APIRouter

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.dashboard import (
    ExecutiveDashboard,
    ComplianceDashboard,
    SecurityDashboard,
    AuditReadinessDashboard,
    ControlOwnerDashboard,
)
from app.services import dashboard_service

router = APIRouter(
    prefix="/organizations/{org_id}/dashboards",
    tags=["dashboards"],
)


@router.get("/executive", response_model=ExecutiveDashboard)
async def executive_dashboard(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Executive dashboard: compliance score, risk heatmap, trends, key metrics."""
    return await dashboard_service.get_executive_dashboard(db, org_id)


@router.get("/compliance", response_model=ComplianceDashboard)
async def compliance_dashboard(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Compliance manager dashboard: framework progress, evidence gaps, policy status."""
    return await dashboard_service.get_compliance_dashboard(db, org_id)


@router.get("/security", response_model=SecurityDashboard)
async def security_dashboard(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Security posture dashboard: scanner results, vulnerability trends."""
    return await dashboard_service.get_security_dashboard(db, org_id)


@router.get("/audit-readiness", response_model=AuditReadinessDashboard)
async def audit_readiness_dashboard(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Audit readiness dashboard: weighted score breakdown."""
    return await dashboard_service.get_audit_readiness_dashboard(db, org_id)


@router.get("/control-owner", response_model=ControlOwnerDashboard)
async def control_owner_dashboard(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Control owner dashboard: controls assigned to the current user."""
    return await dashboard_service.get_control_owner_dashboard(db, org_id, current_user.id)
