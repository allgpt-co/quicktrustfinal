from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, ComplianceUser, AnyInternalUser
from app.schemas.common import PaginatedResponse
from app.schemas.cross_framework_mapping import (
    CrossFrameworkMappingCreate,
    CrossFrameworkMappingResponse,
)
from app.services import cross_framework_mapping_service as mapping_service

router = APIRouter(prefix="/cross-framework-mappings", tags=["cross-framework-mappings"])


@router.get("", response_model=PaginatedResponse)
async def list_mappings(
    db: DB,
    current_user: AnyInternalUser,
    requirement_id: UUID | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await mapping_service.list_mappings(
        db, requirement_id=requirement_id, page=page, page_size=page_size
    )
    return PaginatedResponse(
        items=[CrossFrameworkMappingResponse.model_validate(m) for m in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("", response_model=CrossFrameworkMappingResponse, status_code=201)
async def create_mapping(
    data: CrossFrameworkMappingCreate,
    db: DB,
    current_user: ComplianceUser,
):
    item = await mapping_service.create_mapping(db, data)
    return item


@router.get("/{mapping_id}", response_model=CrossFrameworkMappingResponse)
async def get_mapping(
    mapping_id: UUID,
    db: DB,
    current_user: AnyInternalUser,
):
    return await mapping_service.get_mapping(db, mapping_id)


@router.delete("/{mapping_id}", status_code=204)
async def delete_mapping(
    mapping_id: UUID,
    db: DB,
    current_user: ComplianceUser,
):
    await mapping_service.delete_mapping(db, mapping_id)
