from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PolicyAcknowledgmentCreate(BaseModel):
    policy_id: UUID
    user_id: UUID
    due_date: datetime | None = None


class PolicyAcknowledgmentResponse(BaseModel):
    id: UUID
    org_id: UUID
    policy_id: UUID
    user_id: UUID
    policy_version: str
    status: str
    acknowledged_at: datetime | None
    due_date: datetime | None
    ip_address: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AcknowledgeRequest(BaseModel):
    notes: str | None = None


class PolicyAcknowledgmentStats(BaseModel):
    total: int
    acknowledged: int
    pending: int
    overdue: int
    acknowledgment_rate: float
