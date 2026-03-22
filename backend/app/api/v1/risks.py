from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.risk import (
    RiskCreate,
    RiskUpdate,
    RiskResponse,
    RiskStatsResponse,
    RiskMatrixResponse,
    RiskControlMappingCreate,
    RiskControlMappingResponse,
)
from app.services import risk_service

router = APIRouter(
    prefix="/organizations/{org_id}/risks",
    tags=["risks"],
)


@router.get("", response_model=PaginatedResponse)
async def list_risks(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = None,
    risk_level: str | None = None,
    category: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await risk_service.list_risks(
        db, org_id, status=status, risk_level=risk_level,
        category=category, page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[RiskResponse.model_validate(i) for i in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=RiskResponse, status_code=201)
async def create_risk(org_id: VerifiedOrgId, data: RiskCreate, db: DB, current_user: ComplianceUser):
    item = await risk_service.create_risk(db, org_id, data)
    await log_audit(db, current_user, "create", "risk", str(item.id), org_id)
    return item


@router.get("/stats", response_model=RiskStatsResponse)
async def get_risk_stats(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    return await risk_service.get_risk_stats(db, org_id)


@router.get("/matrix", response_model=RiskMatrixResponse)
async def get_risk_matrix(org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser):
    cells = await risk_service.get_risk_matrix(db, org_id)
    return RiskMatrixResponse(cells=cells)


@router.get("/{risk_id}", response_model=RiskResponse)
async def get_risk(org_id: VerifiedOrgId, risk_id: UUID, db: DB, current_user: AnyInternalUser):
    return await risk_service.get_risk(db, org_id, risk_id)


@router.patch("/{risk_id}", response_model=RiskResponse)
async def update_risk(
    org_id: VerifiedOrgId, risk_id: UUID, data: RiskUpdate, db: DB, current_user: ComplianceUser
):
    item = await risk_service.update_risk(db, org_id, risk_id, data)
    await log_audit(db, current_user, "update", "risk", str(risk_id), org_id)
    return item


@router.delete("/{risk_id}", status_code=204)
async def delete_risk(org_id: VerifiedOrgId, risk_id: UUID, db: DB, current_user: ComplianceUser):
    await risk_service.delete_risk(db, org_id, risk_id)
    await log_audit(db, current_user, "delete", "risk", str(risk_id), org_id)


@router.post("/{risk_id}/controls", response_model=RiskControlMappingResponse, status_code=201)
async def add_control_mapping(
    org_id: VerifiedOrgId, risk_id: UUID, data: RiskControlMappingCreate,
    db: DB, current_user: ComplianceUser,
):
    item = await risk_service.add_control_mapping(db, org_id, risk_id, data)
    await log_audit(db, current_user, "add_control_mapping", "risk", str(risk_id), org_id)
    return item


@router.delete("/{risk_id}/controls/{mapping_id}", status_code=204)
async def remove_control_mapping(
    org_id: VerifiedOrgId, risk_id: UUID, mapping_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await risk_service.remove_control_mapping(db, org_id, risk_id, mapping_id)
    await log_audit(db, current_user, "remove_control_mapping", "risk", str(risk_id), org_id)


# --- Risk Acceptance Workflow ---

class RiskAcceptanceRequest(BaseModel):
    justification: str
    expiry_date: datetime | None = None

class RiskAcceptanceDecision(BaseModel):
    approved: bool
    reason: str | None = None


@router.post("/{risk_id}/accept", response_model=RiskResponse)
async def request_risk_acceptance(
    org_id: VerifiedOrgId, risk_id: UUID, data: RiskAcceptanceRequest,
    db: DB, current_user: AnyInternalUser,
):
    """Request risk acceptance — requires manager/admin approval."""
    risk = await risk_service.get_risk(db, org_id, risk_id)
    risk.acceptance_status = "pending"
    risk.acceptance_requested_by = current_user.id
    risk.acceptance_requested_at = datetime.now(timezone.utc)
    risk.acceptance_justification = data.justification
    if data.expiry_date:
        risk.acceptance_expiry = data.expiry_date
    risk.treatment_type = "accept"
    await db.commit()
    await db.refresh(risk)
    await log_audit(db, current_user, "request_acceptance", "risk", str(risk_id), org_id)
    return risk


@router.post("/{risk_id}/accept/decide", response_model=RiskResponse)
async def decide_risk_acceptance(
    org_id: VerifiedOrgId, risk_id: UUID, data: RiskAcceptanceDecision,
    db: DB, current_user: ComplianceUser,
):
    """Approve or reject a risk acceptance request. Requires compliance_manager+ role."""
    risk = await risk_service.get_risk(db, org_id, risk_id)
    if risk.acceptance_status != "pending":
        from fastapi import HTTPException
        raise HTTPException(400, "No pending acceptance request for this risk")
    risk.acceptance_status = "approved" if data.approved else "rejected"
    risk.acceptance_approved_by = current_user.id
    risk.acceptance_approved_at = datetime.now(timezone.utc)
    if data.approved:
        risk.status = "accepted"
    await db.commit()
    await db.refresh(risk)
    action = "approve_acceptance" if data.approved else "reject_acceptance"
    await log_audit(db, current_user, action, "risk", str(risk_id), org_id)
    return risk
