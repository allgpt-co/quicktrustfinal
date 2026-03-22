"""Pydantic schemas for control test execution engine."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ControlTestDefinitionCreate(BaseModel):
    control_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    collector_type: str = Field(..., min_length=1, max_length=100)
    assertion_field: str = Field(..., min_length=1, max_length=255)
    assertion_operator: str = Field(default="eq", pattern="^(eq|neq|gt|gte|lt|lte|contains|not_contains|exists)$")
    assertion_value: str = Field(..., max_length=500)
    schedule: str = Field(default="daily", pattern="^(hourly|daily|weekly)$")
    is_active: bool = True
    integration_id: UUID | None = None


class ControlTestDefinitionResponse(BaseModel):
    id: UUID
    org_id: UUID
    control_id: UUID
    name: str
    description: str | None
    collector_type: str
    assertion_field: str
    assertion_operator: str
    assertion_value: str
    schedule: str
    is_active: bool
    integration_id: UUID | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ControlTestResultResponse(BaseModel):
    id: UUID
    org_id: UUID
    test_definition_id: UUID
    control_id: UUID
    result: str
    actual_value: str | None
    expected_value: str
    evidence_id: UUID | None
    duration_ms: int | None
    error_message: str | None
    details: dict | None
    executed_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class ControlTestSummaryResponse(BaseModel):
    total_runs: int
    passed: int
    failed: int
    pass_rate: float
    last_result: str | None
    last_tested_at: str | None


class ScheduleConfigRequest(BaseModel):
    schedule: str = Field(..., pattern="^(hourly|daily|weekly)$")
    collector_type: str = Field(..., min_length=1, max_length=100)
    control_id: UUID | None = None
