"""Schemas for GDPR / data-retention endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Data Retention Policies
# ---------------------------------------------------------------------------
class DataRetentionPolicyCreate(BaseModel):
    entity_type: str
    retention_days: int
    description: str | None = None
    is_active: bool = True


class DataRetentionPolicyResponse(BaseModel):
    id: UUID
    org_id: UUID
    entity_type: str
    retention_days: int
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Deletion Requests (GDPR Right to Erasure)
# ---------------------------------------------------------------------------
class DeletionRequestCreate(BaseModel):
    target_user_id: UUID
    reason: str | None = None


class DeletionRequestResponse(BaseModel):
    id: UUID
    org_id: UUID
    requested_by: UUID
    target_user_id: UUID
    status: str
    reason: str | None
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Data Export (GDPR Right of Access)
# ---------------------------------------------------------------------------
class DataExportResponse(BaseModel):
    user_id: UUID
    email: str
    full_name: str
    role: str
    org_id: UUID
    audit_log_count: int
    evidence_count: int
    agent_run_count: int
    exported_at: datetime
