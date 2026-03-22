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


@router.get("/compliance-posture")
async def compliance_posture(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    """Compliance posture: per-framework control assessment summary with maturity."""
    from sqlalchemy import select, func
    from app.models.control import Control
    from app.models.control_framework_mapping import ControlFrameworkMapping
    from app.models.framework import Framework

    # Get all frameworks (frameworks are global, not org-scoped)
    fw_q = select(Framework).where(Framework.is_active.is_(True))
    frameworks = list((await db.execute(fw_q)).scalars().all())

    posture = []
    for fw in frameworks:
        mapped_q = (
            select(Control)
            .join(ControlFrameworkMapping, ControlFrameworkMapping.control_id == Control.id)
            .where(ControlFrameworkMapping.framework_id == fw.id, Control.org_id == org_id)
        )
        controls = list((await db.execute(mapped_q)).scalars().all())
        total = len(controls)
        passed = sum(1 for c in controls if c.last_test_result == "pass")
        failed = sum(1 for c in controls if c.last_test_result == "fail")
        implemented = sum(1 for c in controls if c.status == "implemented")
        avg_maturity = 0.0
        maturity_controls = [c for c in controls if c.maturity_level is not None]
        if maturity_controls:
            avg_maturity = round(sum(c.maturity_level for c in maturity_controls) / len(maturity_controls), 1)

        posture.append({
            "framework": fw.name,
            "framework_id": str(fw.id),
            "total_controls": total,
            "implemented": implemented,
            "passed": passed,
            "failed": failed,
            "not_assessed": total - passed - failed,
            "score": round((implemented / total) * 100) if total > 0 else 0,
            "avg_maturity": avg_maturity,
        })

    return {"posture": posture}
