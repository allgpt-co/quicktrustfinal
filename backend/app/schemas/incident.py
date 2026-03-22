from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.enums import IncidentSeverity, IncidentStatus


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    severity: IncidentSeverity = IncidentSeverity.P3
    status: IncidentStatus = IncidentStatus.OPEN
    category: str | None = None
    assigned_to_id: UUID | None = None
    detected_at: datetime | None = None
    related_control_ids: list[str] | None = None


class IncidentUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=500)
    description: str | None = Field(None, max_length=5000)
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None
    category: str | None = None
    assigned_to_id: UUID | None = None
    detected_at: datetime | None = None
    contained_at: datetime | None = None
    resolved_at: datetime | None = None
    closed_at: datetime | None = None
    post_mortem_notes: str | None = None
    root_cause: str | None = None
    lessons_learned: str | None = None
    related_control_ids: list[str] | None = None
    breach_notification_required: bool | None = None
    breach_notified_at: datetime | None = None
    affected_users_count: int | None = None
    affected_systems: list[str] | None = None


class TimelineEventCreate(BaseModel):
    event_type: str = "note"
    description: str = Field(..., min_length=1)
    occurred_at: datetime | None = None


class TimelineEventResponse(BaseModel):
    id: UUID
    incident_id: UUID
    actor_id: UUID | None
    event_type: str
    description: str
    occurred_at: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


class IncidentResponse(BaseModel):
    id: UUID
    org_id: UUID
    title: str
    description: str | None
    severity: str
    status: str
    category: str | None
    assigned_to_id: UUID | None
    detected_at: datetime | None
    contained_at: datetime | None = None
    resolved_at: datetime | None
    closed_at: datetime | None = None
    post_mortem_notes: str | None
    root_cause: str | None = None
    lessons_learned: str | None = None
    related_control_ids: list | None
    breach_notification_required: bool = False
    breach_notification_deadline: datetime | None = None
    breach_notified_at: datetime | None = None
    affected_users_count: int = 0
    affected_systems: list | None = None
    timeline_events: list[TimelineEventResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentStatsResponse(BaseModel):
    total: int = 0
    by_status: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    open_p1_count: int = 0
    avg_resolution_hours: float = 0.0
