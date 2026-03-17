from uuid import UUID

from fastapi import APIRouter, Query, Request

from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, CurrentUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.policy_acknowledgment import (
    PolicyAcknowledgmentCreate,
    PolicyAcknowledgmentResponse,
    AcknowledgeRequest,
    PolicyAcknowledgmentStats,
)
from app.services import policy_acknowledgment_service

router = APIRouter(
    prefix="/organizations/{org_id}/policy-acknowledgments",
    tags=["policy-acknowledgments"],
)


@router.get("", response_model=PaginatedResponse)
async def list_acknowledgments(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    policy_id: UUID | None = None,
    user_id: UUID | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await policy_acknowledgment_service.list_acknowledgments(
        db, org_id, policy_id=policy_id, user_id=user_id, status=status,
        page=page, page_size=page_size,
    )
    return PaginatedResponse(
        items=[PolicyAcknowledgmentResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=PolicyAcknowledgmentResponse, status_code=201)
async def request_acknowledgment(
    org_id: VerifiedOrgId, data: PolicyAcknowledgmentCreate,
    db: DB, current_user: ComplianceUser,
):
    return await policy_acknowledgment_service.request_acknowledgment(
        db, org_id, data.policy_id, data.user_id, data.due_date
    )


@router.post("/bulk", status_code=200)
async def bulk_request(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
    policy_id: UUID = Query(...),
    user_ids: list[UUID] = Query(...),
    due_date: str | None = None,
):
    from datetime import datetime
    dd = datetime.fromisoformat(due_date) if due_date else None
    count = await policy_acknowledgment_service.bulk_request_acknowledgment(
        db, org_id, policy_id, user_ids, dd
    )
    return {"created": count}


@router.get("/stats", response_model=PolicyAcknowledgmentStats)
async def get_stats(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    policy_id: UUID | None = None,
):
    return await policy_acknowledgment_service.get_stats(db, org_id, policy_id)


@router.post("/{acknowledgment_id}/acknowledge", response_model=PolicyAcknowledgmentResponse)
async def acknowledge(
    org_id: VerifiedOrgId, acknowledgment_id: UUID,
    data: AcknowledgeRequest, request: Request,
    db: DB, current_user: CurrentUser,
):
    ip = request.client.host if request.client else None
    return await policy_acknowledgment_service.acknowledge(
        db, org_id, acknowledgment_id, current_user.id, ip_address=ip, notes=data.notes
    )


@router.get("/my-pending", response_model=list[PolicyAcknowledgmentResponse])
async def my_pending(
    org_id: VerifiedOrgId, db: DB, current_user: CurrentUser,
):
    items, _ = await policy_acknowledgment_service.list_acknowledgments(
        db, org_id, user_id=current_user.id, status="pending", page=1, page_size=100
    )
    return [PolicyAcknowledgmentResponse.model_validate(i) for i in items]
