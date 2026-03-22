"""Pydantic schemas for drift detection."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class DriftBaselineResponse(BaseModel):
    id: UUID
    org_id: UUID
    resource_type: str
    resource_id: UUID
    baseline_hash: str
    finding_count: int
    captured_at: datetime
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class DriftEventResponse(BaseModel):
    id: UUID
    org_id: UUID
    baseline_id: UUID
    resource_type: str
    resource_id: UUID
    drift_type: str
    severity: str
    title: str
    description: str | None
    previous_value: dict | None
    current_value: dict | None
    status: str
    acknowledged_by: UUID | None
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DriftSummaryResponse(BaseModel):
    total_events: int
    open_events: int
    critical_high_open: int
