from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.enums import EvidenceStatus


class EvidenceCreate(BaseModel):
    control_id: UUID
    template_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    status: EvidenceStatus = EvidenceStatus.PENDING
    artifact_url: str | None = None
    data: dict | None = None
    collection_method: str = "manual"
    collector: str | None = None


class EvidenceReject(BaseModel):
    reason: str = Field(..., min_length=1, max_length=1000)


class EvidenceResponse(BaseModel):
    id: UUID
    org_id: UUID
    control_id: UUID
    template_id: UUID | None
    title: str
    status: str
    collected_at: datetime | None
    expires_at: datetime | None
    artifact_url: str | None
    artifact_hash: str | None
    file_url: str | None = None
    file_name: str | None = None
    data: dict | None
    collection_method: str
    collector: str | None
    data_source: str | None = None
    collected_by: UUID | None = None
    reviewed_by: UUID | None = None
    reviewed_at: datetime | None = None
    approved_by: UUID | None = None
    approved_at: datetime | None = None
    rejected_by: UUID | None = None
    rejected_at: datetime | None = None
    rejection_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
