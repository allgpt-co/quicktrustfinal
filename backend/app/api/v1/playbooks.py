from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, ComplianceUser, AnyInternalUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.playbook import (
    PlaybookCreate,
    PlaybookUpdate,
    PlaybookResponse,
    PlaybookExecutionResponse,
    StepCompleteRequest,
)
from app.services import playbook_service

router = APIRouter(
    prefix="/organizations/{org_id}/playbooks",
    tags=["playbooks"],
)


@router.get("", response_model=PaginatedResponse)
async def list_playbooks(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    items, total = await playbook_service.list_playbooks(db, org_id, page, page_size)
    return PaginatedResponse(
        items=[PlaybookResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/seed-defaults", status_code=200)
async def seed_defaults(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
):
    count = await playbook_service.seed_default_playbooks(db, org_id)
    return {"seeded": count, "message": f"{count} default playbooks created" if count else "Default playbooks already exist"}


@router.post("", response_model=PlaybookResponse, status_code=201)
async def create_playbook(
    org_id: VerifiedOrgId, data: PlaybookCreate,
    db: DB, current_user: ComplianceUser,
):
    return await playbook_service.create_playbook(db, org_id, data)


@router.get("/{playbook_id}", response_model=PlaybookResponse)
async def get_playbook(
    org_id: VerifiedOrgId, playbook_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    return await playbook_service.get_playbook(db, org_id, playbook_id)


@router.patch("/{playbook_id}", response_model=PlaybookResponse)
async def update_playbook(
    org_id: VerifiedOrgId, playbook_id: UUID,
    data: PlaybookUpdate, db: DB, current_user: ComplianceUser,
):
    return await playbook_service.update_playbook(db, org_id, playbook_id, data)


@router.delete("/{playbook_id}", status_code=204)
async def delete_playbook(
    org_id: VerifiedOrgId, playbook_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await playbook_service.delete_playbook(db, org_id, playbook_id)


@router.post("/{playbook_id}/trigger/{incident_id}", response_model=PlaybookExecutionResponse)
async def trigger_playbook(
    org_id: VerifiedOrgId, playbook_id: UUID, incident_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    return await playbook_service.trigger_playbook(db, org_id, playbook_id, incident_id)


@router.get("/executions/by-incident/{incident_id}", response_model=list[PlaybookExecutionResponse])
async def list_executions_by_incident(
    org_id: VerifiedOrgId, incident_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    return [
        PlaybookExecutionResponse.model_validate(e)
        for e in await playbook_service.list_executions(db, org_id, incident_id=incident_id)
    ]


@router.post("/executions/{execution_id}/complete-step", response_model=PlaybookExecutionResponse)
async def complete_step(
    org_id: VerifiedOrgId, execution_id: UUID,
    data: StepCompleteRequest, db: DB, current_user: ComplianceUser,
):
    return await playbook_service.complete_step(
        db, org_id, execution_id, completed_by_id=current_user.id, notes=data.notes
    )
