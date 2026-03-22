from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    id: UUID
    org_id: UUID
    event_type: str | None = None
    event_category: str | None = None
    severity: str | None = None
    actor_type: str
    actor_id: str
    actor_email: str | None = None
    actor_role: str | None = None
    actor_ip: str | None = None
    actor_user_agent: str | None = None
    action: str
    entity_type: str
    entity_id: str
    outcome: str | None = None
    changes: dict | None = None
    ip_address: str | None = None
    request_id: str | None = None
    session_id: str | None = None
    timestamp: datetime

    model_config = {"from_attributes": True}


class AuditLogStatsResponse(BaseModel):
    total: int
    by_action: dict[str, int]
    by_category: dict[str, int] = {}
    by_severity: dict[str, int] = {}
