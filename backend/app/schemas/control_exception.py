from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ControlExceptionCreate(BaseModel):
    control_id: UUID
    title: str = Field(..., min_length=1, max_length=500)
    reason: str = Field(..., min_length=1)
    compensating_control: str | None = None
    risk_acceptance: str | None = None
    expires_at: datetime | None = None


class ControlExceptionUpdate(BaseModel):
    title: str | None = None
    reason: str | None = None
    compensating_control: str | None = None
    risk_acceptance: str | None = None
    expires_at: datetime | None = None


class ControlExceptionApprove(BaseModel):
    expires_at: datetime | None = None


class ControlExceptionDeny(BaseModel):
    denial_reason: str = Field(..., min_length=1)


class ControlExceptionResponse(BaseModel):
    id: UUID
    org_id: UUID
    control_id: UUID
    title: str
    reason: str
    compensating_control: str | None
    risk_acceptance: str | None
    status: str
    requested_by_id: UUID | None
    approved_by_id: UUID | None
    approved_at: datetime | None
    denied_by_id: UUID | None
    denied_at: datetime | None
    denial_reason: str | None
    expires_at: datetime | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
