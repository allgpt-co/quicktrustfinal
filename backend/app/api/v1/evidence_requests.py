from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from sqlalchemy import select

from app.core.dependencies import (
    DB,
    AnyInternalUser,
    ComplianceUser,
    VerifiedOrgId,
)
from app.core.exceptions import NotFoundError
from app.models.evidence_request import EvidenceRequest

router = APIRouter(
    prefix="/organizations/{org_id}/evidence-requests",
    tags=["evidence-requests"],
)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------
class EvidenceRequestCreate(PydanticBaseModel):
    title: str
    description: str | None = None
    control_id: UUID | None = None
    audit_id: UUID | None = None
    deadline: datetime | None = None
    assigned_to: UUID | None = None


class EvidenceRequestUpdate(PydanticBaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    deadline: datetime | None = None
    assigned_to: UUID | None = None
    evidence_id: UUID | None = None


class UserSummary(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str | None = None
    full_name: str | None = None


class EvidenceRequestResponse(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    org_id: UUID
    audit_id: UUID | None
    control_id: UUID | None
    title: str
    description: str | None
    status: str
    deadline: datetime | None
    submitted_at: datetime | None
    evidence_id: UUID | None
    requested_by: UUID
    assigned_to: UUID | None
    created_at: datetime
    updated_at: datetime
    requester: UserSummary | None = None
    assignee: UserSummary | None = None


def _serialize(item: EvidenceRequest) -> EvidenceRequestResponse:
    return EvidenceRequestResponse.model_validate(item)


async def _get_request_or_404(
    db, org_id: UUID, request_id: UUID
) -> EvidenceRequest:
    result = await db.execute(
        select(EvidenceRequest).where(
            EvidenceRequest.id == request_id,
            EvidenceRequest.org_id == org_id,
            EvidenceRequest.deleted_at.is_(None),
        )
    )
    item = result.scalar_one_or_none()
    if item is None:
        raise NotFoundError(f"Evidence request {request_id} not found")
    return item


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.post("", response_model=EvidenceRequestResponse, status_code=201)
async def create_evidence_request(
    org_id: VerifiedOrgId,
    data: EvidenceRequestCreate,
    db: DB,
    current_user: ComplianceUser,
) -> EvidenceRequestResponse:
    request_obj = EvidenceRequest(
        org_id=org_id,
        audit_id=data.audit_id,
        control_id=data.control_id,
        requested_by=current_user.id,
        assigned_to=data.assigned_to,
        title=data.title,
        description=data.description,
        deadline=data.deadline,
        status="pending",
    )
    db.add(request_obj)
    await db.commit()
    await db.refresh(request_obj)
    return _serialize(request_obj)


@router.get("", response_model=list[EvidenceRequestResponse])
async def list_evidence_requests(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    status: str | None = Query(None),
) -> list[EvidenceRequestResponse]:
    stmt = select(EvidenceRequest).where(
        EvidenceRequest.org_id == org_id,
        EvidenceRequest.deleted_at.is_(None),
    )
    if status is not None:
        stmt = stmt.where(EvidenceRequest.status == status)
    stmt = stmt.order_by(EvidenceRequest.created_at.desc())

    result = await db.execute(stmt)
    items = list(result.scalars().all())
    return [_serialize(item) for item in items]


@router.get("/{request_id}", response_model=EvidenceRequestResponse)
async def get_evidence_request(
    org_id: VerifiedOrgId,
    request_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
) -> EvidenceRequestResponse:
    item = await _get_request_or_404(db, org_id, request_id)
    return _serialize(item)


@router.patch("/{request_id}", response_model=EvidenceRequestResponse)
async def update_evidence_request(
    org_id: VerifiedOrgId,
    request_id: UUID,
    data: EvidenceRequestUpdate,
    db: DB,
    current_user: ComplianceUser,
) -> EvidenceRequestResponse:
    item = await _get_request_or_404(db, org_id, request_id)

    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(item, field, value)

    # Auto-set submitted_at when status transitions to submitted
    if updates.get("status") == "submitted" and item.submitted_at is None:
        item.submitted_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(item)
    return _serialize(item)


@router.delete("/{request_id}", status_code=204)
async def delete_evidence_request(
    org_id: VerifiedOrgId,
    request_id: UUID,
    db: DB,
    current_user: ComplianceUser,
) -> None:
    item = await _get_request_or_404(db, org_id, request_id)
    item.deleted_at = datetime.now(timezone.utc)
    await db.commit()
