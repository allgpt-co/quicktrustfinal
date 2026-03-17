from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PlaybookStep(BaseModel):
    order: int
    title: str
    description: str
    assignee_role: str | None = None
    sla_hours: int | None = None


class PlaybookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    severity_trigger: str | None = None
    category_trigger: str | None = None
    steps: list[PlaybookStep] = []
    notification_channels: list[str] = []
    compliance_references: list[str] = []


class PlaybookUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity_trigger: str | None = None
    category_trigger: str | None = None
    is_active: bool | None = None
    steps: list[PlaybookStep] | None = None
    notification_channels: list[str] | None = None
    compliance_references: list[str] | None = None


class PlaybookResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    severity_trigger: str | None
    category_trigger: str | None
    is_default: bool
    is_active: bool
    steps: list | None
    notification_channels: list | None
    compliance_references: list | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PlaybookExecutionResponse(BaseModel):
    id: UUID
    org_id: UUID
    playbook_id: UUID
    incident_id: UUID
    status: str
    current_step: int
    step_statuses: list | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StepCompleteRequest(BaseModel):
    notes: str | None = None
