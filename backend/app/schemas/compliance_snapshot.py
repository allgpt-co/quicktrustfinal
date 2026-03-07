from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ComplianceSnapshotCreate(BaseModel):
    framework_id: UUID
    triggered_by: Literal["manual", "scheduled", "audit_start"] = "manual"


class ComplianceSnapshotResponse(BaseModel):
    id: UUID
    org_id: UUID
    framework_id: UUID
    snapshot_date: datetime
    total_controls: int
    implemented_controls: int
    implementation_percentage: float
    evidence_coverage_percentage: float
    risk_score_avg: float | None
    details: dict | None
    triggered_by: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
