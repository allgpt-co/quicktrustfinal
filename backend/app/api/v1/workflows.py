"""API endpoints for durable workflow execution tracking."""
from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel as PydanticModel

from app.core.dependencies import DB, AnyInternalUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.services import workflow_service

router = APIRouter(
    prefix="/organizations/{org_id}/workflows",
    tags=["workflows"],
)


class WorkflowResponse(PydanticModel):
    id: UUID
    org_id: UUID
    workflow_type: str
    reference_id: UUID | None
    status: str
    current_step: int
    total_steps: int
    step_name: str | None
    input_data: dict | None
    output_data: dict | None
    error_message: str | None
    retry_count: int
    max_retries: int
    started_at: str | None
    completed_at: str | None
    triggered_by: UUID | None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


@router.get("", response_model=PaginatedResponse)
async def list_workflows(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    workflow_type: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await workflow_service.list_workflows(
        db, org_id, workflow_type, status, page, page_size
    )
    return PaginatedResponse(
        items=[WorkflowResponse.model_validate(w) for w in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    org_id: VerifiedOrgId, workflow_id: UUID, db: DB, current_user: AnyInternalUser,
):
    wf = await workflow_service.get_workflow(db, workflow_id)
    if not wf:
        from app.core.exceptions import NotFoundError
        raise NotFoundError(f"Workflow {workflow_id} not found")
    return wf
