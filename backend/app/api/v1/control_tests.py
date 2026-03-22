"""API endpoints for control test execution engine."""
from uuid import UUID

from fastapi import APIRouter, Query

from app.core.audit_middleware import log_audit
from app.core.dependencies import DB, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.schemas.common import PaginatedResponse
from app.schemas.control_test import (
    ControlTestDefinitionCreate,
    ControlTestDefinitionResponse,
    ControlTestResultResponse,
    ControlTestSummaryResponse,
)
from app.services import control_test_service

router = APIRouter(
    prefix="/organizations/{org_id}/control-tests",
    tags=["control-tests"],
)


# --- Test Definitions ---

@router.get("/definitions", response_model=PaginatedResponse)
async def list_definitions(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    control_id: UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await control_test_service.list_test_definitions(
        db, org_id, control_id, page, page_size
    )
    return PaginatedResponse(
        items=[ControlTestDefinitionResponse.model_validate(d) for d in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.post("/definitions", response_model=ControlTestDefinitionResponse, status_code=201)
async def create_definition(
    org_id: VerifiedOrgId, data: ControlTestDefinitionCreate,
    db: DB, current_user: ComplianceUser,
):
    defn = await control_test_service.create_test_definition(db, org_id, data.model_dump())
    await log_audit(db, current_user, "create", "control_test_definition", str(defn.id), org_id)
    return defn


@router.get("/definitions/{definition_id}", response_model=ControlTestDefinitionResponse)
async def get_definition(
    org_id: VerifiedOrgId, definition_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    return await control_test_service.get_test_definition(db, org_id, definition_id)


@router.delete("/definitions/{definition_id}", status_code=204)
async def delete_definition(
    org_id: VerifiedOrgId, definition_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    await control_test_service.delete_test_definition(db, org_id, definition_id)
    await log_audit(db, current_user, "delete", "control_test_definition", str(definition_id), org_id)


# --- Execute Tests ---

@router.post("/definitions/{definition_id}/run", response_model=ControlTestResultResponse)
async def run_test(
    org_id: VerifiedOrgId, definition_id: UUID,
    db: DB, current_user: ComplianceUser,
):
    """Execute a single control test on demand."""
    defn = await control_test_service.get_test_definition(db, org_id, definition_id)
    result = await control_test_service.execute_test(db, org_id, defn)
    await log_audit(db, current_user, "execute", "control_test", str(definition_id), org_id)
    return result


@router.post("/run-all")
async def run_all_tests(
    org_id: VerifiedOrgId, db: DB, current_user: ComplianceUser,
):
    """Execute all active control tests for this organization."""
    count = await control_test_service.run_all_due_tests(db)
    return {"executed": count, "message": f"Executed {count} control tests"}


# --- Test Results ---

@router.get("/results", response_model=PaginatedResponse)
async def list_results(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    control_id: UUID | None = Query(None),
    definition_id: UUID | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
):
    items, total = await control_test_service.list_test_results(
        db, org_id, control_id, definition_id, page, page_size
    )
    return PaginatedResponse(
        items=[ControlTestResultResponse.model_validate(r) for r in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/controls/{control_id}/summary", response_model=ControlTestSummaryResponse)
async def control_test_summary(
    org_id: VerifiedOrgId, control_id: UUID,
    db: DB, current_user: AnyInternalUser,
):
    return await control_test_service.get_control_test_summary(db, org_id, control_id)
