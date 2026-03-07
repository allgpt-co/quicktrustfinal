from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.compliance_snapshot import (
    ComplianceSnapshotCreate,
    ComplianceSnapshotResponse,
)
from app.services import compliance_snapshot_service as snapshot_service

router = APIRouter(
    prefix="/organizations/{org_id}/compliance-snapshots",
    tags=["compliance-snapshots"],
)


@router.get("", response_model=PaginatedResponse)
async def list_snapshots(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    framework_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await snapshot_service.list_snapshots(
        db, org_id, framework_id=framework_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[ComplianceSnapshotResponse.model_validate(s) for s in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ComplianceSnapshotResponse, status_code=201)
async def create_snapshot(
    org_id: VerifiedOrgId,
    data: ComplianceSnapshotCreate,
    db: DB,
    current_user: ComplianceUser,
):
    item = await snapshot_service.create_snapshot(
        db, org_id, data.framework_id, triggered_by=data.triggered_by
    )
    await log_audit(db, current_user, "create", "compliance_snapshot", str(item.id), org_id)
    return item


@router.get("/{snapshot_id}", response_model=ComplianceSnapshotResponse)
async def get_snapshot(
    org_id: VerifiedOrgId,
    snapshot_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
):
    return await snapshot_service.get_snapshot(db, org_id, snapshot_id)
