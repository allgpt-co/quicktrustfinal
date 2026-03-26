from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class FrameworkResponse(BaseModel):
    id: UUID
    name: str
    version: str
    category: str | None
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FrameworkDomainResponse(BaseModel):
    id: UUID
    framework_id: UUID
    code: str
    name: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FrameworkRequirementResponse(BaseModel):
    id: UUID
    domain_id: UUID
    code: str
    title: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ControlObjectiveResponse(BaseModel):
    id: UUID
    requirement_id: UUID
    code: str
    title: str
    description: str | None
    sort_order: int
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Create / Update schemas ---

class FrameworkCreate(BaseModel):
    name: str
    version: str
    category: str | None = None
    description: str | None = None


class FrameworkUpdate(BaseModel):
    name: str | None = None
    version: str | None = None
    category: str | None = None
    description: str | None = None
    is_active: bool | None = None


class DomainCreate(BaseModel):
    code: str
    name: str
    description: str | None = None


class RequirementCreate(BaseModel):
    code: str
    title: str
    description: str | None = None


class FrameworkDetailResponse(FrameworkResponse):
    domains: list[FrameworkDomainResponse] = []


class DomainDetailResponse(FrameworkDomainResponse):
    requirements: list[FrameworkRequirementResponse] = []


class RequirementDetailResponse(FrameworkRequirementResponse):
    objectives: list[ControlObjectiveResponse] = []


# --- Framework versioning schemas ---


class VersionRequirementInput(BaseModel):
    """A requirement to include in a new framework version."""
    domain_code: str
    domain_name: str
    domain_description: str | None = None
    code: str
    title: str
    description: str | None = None


class FrameworkVersionCreate(BaseModel):
    """Payload for creating a new version of an existing framework."""
    version: str
    description: str | None = None
    requirements: list[VersionRequirementInput] = []


class FrameworkVersionResponse(FrameworkResponse):
    previous_version_id: UUID | None = None


class DiffRequirementItem(BaseModel):
    """A single requirement that was added, removed, or modified between versions."""
    code: str
    title: str
    changes: dict | None = None  # For modified items: field -> {old, new}


class FrameworkDiffResponse(BaseModel):
    """Result of diffing two framework versions."""
    source_framework_id: UUID
    source_version: str
    target_framework_id: UUID
    target_version: str
    added: list[DiffRequirementItem] = []
    removed: list[DiffRequirementItem] = []
    modified: list[DiffRequirementItem] = []
