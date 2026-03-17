from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.control_exception import (
    ControlExceptionCreate,
    ControlExceptionUpdate,
    ControlExceptionApprove,
    ControlExceptionDeny,
    ControlExceptionResponse,
)
from app.services import control_exception_service

router = APIRouter(
    prefix="/organizations/{org_id}/control-exceptions",
    tags=["control-exceptions"],
)


@router.get("", response_model=PaginatedResponse)
async def list_exceptions(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    control_id: UUID | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await control_exception_service.list_exceptions(
        db, org_id, control_id=control_id, status=status, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[ControlExceptionResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=ControlExceptionResponse, status_code=201)
async def create_exception(
    org_id: VerifiedOrgId, data: ControlExceptionCreate,
    db: DB, current_user: ComplianceUser,
):
    return await control_exception_service.create_exception(
        db, org_id, data, requested_by_id=current_user.id
    )


@router.get("/{exception_id}", response_model=ControlExceptionResponse)
async def get_exception(
    org_id: VerifiedOrgId, exception_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    return await control_exception_service.get_exception(db, org_id, exception_id)


@router.patch("/{exception_id}", response_model=ControlExceptionResponse)
async def update_exception(
    org_id: VerifiedOrgId, exception_id: UUID,
    data: ControlExceptionUpdate, db: DB, current_user: ComplianceUser,
):
    return await control_exception_service.update_exception(db, org_id, exception_id, data)


@router.post("/{exception_id}/approve", response_model=ControlExceptionResponse)
async def approve_exception(
    org_id: VerifiedOrgId, exception_id: UUID,
    data: ControlExceptionApprove, db: DB, current_user: ComplianceUser,
):
    return await control_exception_service.approve_exception(
        db, org_id, exception_id, approved_by_id=current_user.id, expires_at=data.expires_at
    )


@router.post("/{exception_id}/deny", response_model=ControlExceptionResponse)
async def deny_exception(
    org_id: VerifiedOrgId, exception_id: UUID,
    data: ControlExceptionDeny, db: DB, current_user: ComplianceUser,
):
    return await control_exception_service.deny_exception(
        db, org_id, exception_id, denied_by_id=current_user.id, denial_reason=data.denial_reason
    )


@router.post("/{exception_id}/revoke", response_model=ControlExceptionResponse)
async def revoke_exception(
    org_id: VerifiedOrgId, exception_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    return await control_exception_service.revoke_exception(db, org_id, exception_id)
