from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

ControlStatus = Literal[
    "draft",
    "not_implemented",
    "in_progress",
    "implemented",
    "not_applicable",
    "needs_review",
]

ControlEffectiveness = Literal[
    "effective",
    "partially_effective",
    "not_effective",
    "not_rated",
]

AutomationLevel = Literal[
    "manual",
    "semi_automated",
    "automated",
]


class ControlCreate(BaseModel):
    template_id: UUID | None = None
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = None
    implementation_details: str | None = None
    owner_id: UUID | None = None
    status: ControlStatus = "draft"
    automation_level: AutomationLevel = "manual"
    test_procedure: str | None = None


class ControlUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    implementation_details: str | None = None
    owner_id: UUID | None = None
    status: ControlStatus | None = None
    effectiveness: ControlEffectiveness | None = None
    automation_level: AutomationLevel | None = None
    test_procedure: str | None = None

    @model_validator(mode="after")
    def check_effectiveness_requires_implemented(self):
        if self.effectiveness and self.status and self.status != "implemented":
            raise ValueError(
                "Effectiveness can only be set when status is 'implemented'"
            )
        return self


class ControlFrameworkMappingResponse(BaseModel):
    id: UUID
    control_id: UUID
    framework_id: UUID
    requirement_id: UUID | None
    objective_id: UUID | None
    framework_name: str | None = None
    requirement_code: str | None = None
    requirement_title: str | None = None

    model_config = {"from_attributes": True}

    @classmethod
    def from_mapping(cls, mapping) -> "ControlFrameworkMappingResponse":
        return cls(
            id=mapping.id,
            control_id=mapping.control_id,
            framework_id=mapping.framework_id,
            requirement_id=mapping.requirement_id,
            objective_id=mapping.objective_id,
            framework_name=mapping.framework.name if mapping.framework else None,
            requirement_code=mapping.requirement.code if mapping.requirement else None,
            requirement_title=mapping.requirement.title if mapping.requirement else None,
        )


class ControlResponse(BaseModel):
    id: UUID
    org_id: UUID
    template_id: UUID | None
    title: str
    description: str | None
    implementation_details: str | None
    owner_id: UUID | None
    status: str
    effectiveness: str | None
    automation_level: str
    test_procedure: str | None
    last_test_date: datetime | None
    last_test_result: str | None
    agent_run_id: UUID | None
    framework_mappings: list[ControlFrameworkMappingResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class BulkApproveRequest(BaseModel):
    control_ids: list[UUID]
    status: ControlStatus = "implemented"


class ControlStatsResponse(BaseModel):
    total: int
    draft: int
    implemented: int
    partially_implemented: int
    not_implemented: int
    not_applicable: int
