import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import GUID, JSONType


class AuditLog(Base):
    """Append-only security audit log. No updates or deletes."""

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, default=uuid.uuid4
    )
    org_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)

    # Event classification
    event_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="GENERAL"
    )
    # AUTH_LOGIN, AUTH_LOGOUT, AUTH_FAILED, AUTH_LOCKED, AUTH_MFA_CHALLENGE,
    # DATA_CREATE, DATA_READ, DATA_UPDATE, DATA_DELETE, DATA_EXPORT,
    # ADMIN_ACTION, SYSTEM_EVENT, AI_AGENT_RUN

    event_category: Mapped[str] = mapped_column(
        String(30), nullable=False, default="system"
    )
    # authentication, authorization, data, admin, system, ai

    severity: Mapped[str] = mapped_column(
        String(10), nullable=False, default="INFO"
    )
    # DEBUG, INFO, WARN, ERROR, CRITICAL

    # Actor info
    actor_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[str] = mapped_column(String(255), nullable=False)
    actor_email: Mapped[str | None] = mapped_column(String(255))
    actor_role: Mapped[str | None] = mapped_column(String(50))
    actor_ip: Mapped[str | None] = mapped_column(String(45))
    actor_user_agent: Mapped[str | None] = mapped_column(Text)

    # What happened
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False)
    outcome: Mapped[str] = mapped_column(
        String(20), nullable=False, default="success"
    )
    # success, failure, denied

    # Details
    changes: Mapped[dict | None] = mapped_column(JSONType(), default=dict)
    # Before/after state, additional context

    # Correlation
    ip_address: Mapped[str | None] = mapped_column(String(45))
    request_id: Mapped[str | None] = mapped_column(String(64))
    session_id: Mapped[str | None] = mapped_column(String(255))

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    __table_args__ = (
        Index("ix_audit_logs_org_timestamp", "org_id", "timestamp"),
        Index("ix_audit_logs_event_type", "event_type", "timestamp"),
        Index("ix_audit_logs_actor", "actor_id", "timestamp"),
        Index("ix_audit_logs_entity", "entity_type", "entity_id"),
        Index("ix_audit_logs_severity", "severity", "timestamp"),
    )
