from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CrossFrameworkMappingCreate(BaseModel):
    requirement_a_id: UUID
    requirement_b_id: UUID
    mapping_type: Literal["equivalent", "partial", "related"]
    notes: str | None = Field(None, max_length=1000)


class CrossFrameworkMappingResponse(BaseModel):
    id: UUID
    requirement_a_id: UUID
    requirement_b_id: UUID
    mapping_type: str
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
