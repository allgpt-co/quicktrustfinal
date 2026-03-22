"""API endpoints for drift detection."""
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.drift import DriftEventResponse, DriftSummaryResponse
from app.services import drift_service

router = APIRouter(
    prefix="/organizations/{org_id}/drift",
    tags=["drift-detection"],
)


@router.get("/events", response_model=PaginatedResponse)
async def list_drift_events(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    resource_type: str | None = Query(None),
    status: str | None = Query(None),
    severity: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await drift_service.list_drift_events(
        db, org_id, resource_type, status, severity, page, page_size
    )
    return PaginatedResponse(
        items=[DriftEventResponse.model_validate(e) for e in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/summary", response_model=DriftSummaryResponse)
async def drift_summary(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
):
    return await drift_service.get_drift_summary(db, org_id)


@router.post("/events/{event_id}/acknowledge", response_model=DriftEventResponse)
async def acknowledge_event(
    org_id: VerifiedOrgId, event_id: UUID, db: DB, current_user: ComplianceUser,
):
    event = await drift_service.acknowledge_drift_event(db, org_id, event_id, current_user.id)
    return event


@router.post("/events/{event_id}/resolve", response_model=DriftEventResponse)
async def resolve_event(
    org_id: VerifiedOrgId, event_id: UUID, db: DB, current_user: ComplianceUser,
):
    event = await drift_service.resolve_drift_event(db, org_id, event_id)
    return event
