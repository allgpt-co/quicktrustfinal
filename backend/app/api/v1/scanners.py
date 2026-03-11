"""Security scanner API endpoints — unified interface for all scanners."""
import logging
from uuid import UUID

from fastapi import APIRouter, Query, Request

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, VerifiedOrgId
from app.core.exceptions import NotFoundError
from app.core.rate_limit import limiter
from app.core.task_runner import create_safe_task
from app.schemas.common import PaginatedResponse
from app.schemas.scan import (
    ScanTrigger,
    ScanResultResponse,
    ScanResultSummary,
    ScanFindingResponse,
    ScanDashboard,
    FindingStatusUpdate,
)
from app.services import scanner_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/organizations/{org_id}/scanners",
    tags=["scanners"],
)


@router.get("/dashboard", response_model=ScanDashboard)
async def get_scanner_dashboard(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
):
    """Get aggregate dashboard stats for all scanners."""
    data = await scanner_service.get_dashboard(db, org_id)
    # Convert recent_scans ORM objects to Pydantic
    data["recent_scans"] = [
        ScanResultSummary.model_validate(s) for s in data["recent_scans"]
    ]
    return data


@router.post("/trigger", response_model=ScanResultResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_scan(
    request: Request,
    org_id: VerifiedOrgId,
    data: ScanTrigger,
    db: DB,
    current_user: ComplianceUser,
):
    """Trigger a security scan. The scan runs asynchronously in the background."""
    scan = await scanner_service.trigger_scan(
        db,
        org_id=org_id,
        scanner_name=data.scanner,
        target=data.target,
        config=data.config,
        triggered_by=current_user.id,
    )

    # Start the scan in background
    create_safe_task(
        scanner_service.execute_scan(scan.id, org_id),
        agent_run_id=scan.id,
        org_id=org_id,
    )

    await log_audit(db, current_user, "trigger_scan", "scan", str(scan.id), org_id)
    return scan


@router.get("/scans", response_model=PaginatedResponse)
async def list_scans(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    scanner: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all scan results with optional filters."""
    items, total = await scanner_service.list_scans(
        db, org_id, scanner=scanner, status=status, page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[ScanResultSummary.model_validate(s) for s in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/scans/{scan_id}", response_model=ScanResultResponse)
async def get_scan(
    org_id: VerifiedOrgId, scan_id: UUID, db: DB, current_user: AnyInternalUser,
):
    """Get a specific scan result."""
    scan = await scanner_service.get_scan(db, org_id, scan_id)
    if not scan:
        raise NotFoundError("Scan not found")
    return scan


@router.get("/findings", response_model=PaginatedResponse)
async def list_findings(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    scan_id: UUID | None = Query(None),
    scanner: str | None = Query(None),
    severity: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    """List scan findings with optional filters."""
    items, total = await scanner_service.list_findings(
        db, org_id,
        scan_id=scan_id, scanner=scanner, severity=severity, status=status,
        page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[ScanFindingResponse.model_validate(f) for f in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.patch("/findings/{finding_id}", response_model=ScanFindingResponse)
async def update_finding_status(
    org_id: VerifiedOrgId,
    finding_id: UUID,
    data: FindingStatusUpdate,
    db: DB,
    current_user: ComplianceUser,
):
    """Update the status of a finding (acknowledge, resolve, mark as false positive)."""
    finding = await scanner_service.update_finding_status(db, org_id, finding_id, data.status)
    if not finding:
        raise NotFoundError("Finding not found")
    await log_audit(db, current_user, "update_finding", "scan_finding", str(finding_id), org_id)
    return finding
