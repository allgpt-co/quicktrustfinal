from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.enums import RiskCategory, RiskTreatment


class RiskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    category: RiskCategory = RiskCategory.OPERATIONAL
    likelihood: int = Field(3, ge=1, le=5)
    impact: int = Field(3, ge=1, le=5)
    status: str = "identified"
    treatment_plan: str | None = Field(None, max_length=5000)
    treatment_type: RiskTreatment | None = None
    treatment_status: str | None = None
    treatment_due_date: datetime | None = None
    residual_likelihood: int | None = Field(None, ge=1, le=5)
    residual_impact: int | None = Field(None, ge=1, le=5)
    owner_id: UUID | None = None
    reviewer_id: UUID | None = None
    next_review_date: datetime | None = None


class RiskUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    category: RiskCategory | None = None
    likelihood: int | None = Field(None, ge=1, le=5)
    impact: int | None = Field(None, ge=1, le=5)
    status: str | None = None
    treatment_plan: str | None = None
    treatment_type: str | None = None
    treatment_status: str | None = None
    treatment_due_date: datetime | None = None
    residual_likelihood: int | None = Field(None, ge=1, le=5)
    residual_impact: int | None = Field(None, ge=1, le=5)
    owner_id: UUID | None = None
    reviewer_id: UUID | None = None
    next_review_date: datetime | None = None


class RiskControlMappingCreate(BaseModel):
    control_id: UUID
    effectiveness: str = "partially_mitigates"
    notes: str | None = None


class RiskControlMappingResponse(BaseModel):
    id: UUID
    risk_id: UUID
    control_id: UUID
    effectiveness: str
    notes: str | None

    model_config = {"from_attributes": True}


class RiskResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    category: str
    likelihood: int
    impact: int
    risk_score: int
    risk_level: str
    status: str
    treatment_plan: str | None
    treatment_type: str | None
    treatment_status: str | None
    treatment_due_date: datetime | None
    residual_likelihood: int | None
    residual_impact: int | None
    residual_score: int | None
    owner_id: UUID | None
    reviewer_id: UUID | None
    last_review_date: datetime | None
    next_review_date: datetime | None
    control_mappings: list[RiskControlMappingResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RiskStatsResponse(BaseModel):
    total: int = 0
    by_status: dict[str, int] = {}
    by_risk_level: dict[str, int] = {}
    average_score: float = 0.0


class RiskMatrixCell(BaseModel):
    likelihood: int
    impact: int
    count: int
    risk_ids: list[str] = []


class RiskMatrixResponse(BaseModel):
    cells: list[RiskMatrixCell] = []
