"""GDPR & data retention API endpoints."""

from uuid import UUID

from fastapi import APIRouter

from app.core.dependencies import CurrentUser, DB, VerifiedOrgId
from app.schemas.privacy import (
    DataExportResponse,
    DataRetentionPolicyCreate,
    DataRetentionPolicyResponse,
    DeletionRequestCreate,
    DeletionRequestResponse,
)
from app.services import privacy_service

router = APIRouter(tags=["privacy"])


# ---------------------------------------------------------------------------
# Data Retention Policies
# ---------------------------------------------------------------------------

@router.get(
    "/organizations/{org_id}/retention-policies",
    response_model=list[DataRetentionPolicyResponse],
)
async def list_retention_policies(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: CurrentUser,
):
    return await privacy_service.list_policies(db, org_id)


@router.post(
    "/organizations/{org_id}/retention-policies",
    response_model=DataRetentionPolicyResponse,
    status_code=201,
)
async def create_retention_policy(
    org_id: VerifiedOrgId,
    body: DataRetentionPolicyCreate,
    db: DB,
    current_user: CurrentUser,
):
    return await privacy_service.create_policy(
        db, org_id, body.entity_type, body.retention_days, body.description
    )


# ---------------------------------------------------------------------------
# GDPR Data Export (Right of Access)
# ---------------------------------------------------------------------------

@router.get("/privacy/data-export", response_model=DataExportResponse)
async def export_my_data(db: DB, current_user: CurrentUser):
    """Export all data associated with the authenticated user."""
    return await privacy_service.export_user_data(db, current_user)


# ---------------------------------------------------------------------------
# GDPR Deletion Requests (Right to Erasure)
# ---------------------------------------------------------------------------

@router.get(
    "/organizations/{org_id}/deletion-requests",
    response_model=list[DeletionRequestResponse],
)
async def list_deletion_requests(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: CurrentUser,
):
    return await privacy_service.list_deletion_requests(db, org_id)


@router.post(
    "/organizations/{org_id}/deletion-requests",
    response_model=DeletionRequestResponse,
    status_code=201,
)
async def create_deletion_request(
    org_id: VerifiedOrgId,
    body: DeletionRequestCreate,
    db: DB,
    current_user: CurrentUser,
):
    return await privacy_service.create_deletion_request(
        db, org_id, current_user.id, body.target_user_id, body.reason
    )


@router.post(
    "/organizations/{org_id}/deletion-requests/{request_id}/process",
    response_model=DeletionRequestResponse,
)
async def process_deletion_request(
    org_id: VerifiedOrgId,
    request_id: UUID,
    db: DB,
    current_user: CurrentUser,
):
    return await privacy_service.process_deletion_request(db, request_id)
