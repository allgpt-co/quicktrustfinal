import uuid

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class IncidentPlaybook(BaseModel):
    __tablename__ = "incident_playbooks"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    severity_trigger: Mapped[str | None] = mapped_column(
        String(20)
    )  # P1, P2, P3, P4 — auto-trigger when incident of this severity is created
    category_trigger: Mapped[str | None] = mapped_column(
        String(100)
    )  # data_breach, ddos, unauthorized_access, malware, insider_threat
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    steps: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # [{order, title, description, assignee_role, sla_hours}]
    notification_channels: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # ["slack:#incident-response", "email:security@company.com"]
    compliance_references: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # ["SOC 2 CC7.3", "GDPR Art. 33"]

    organization = relationship("Organization", lazy="selectin")


class PlaybookExecution(BaseModel):
    __tablename__ = "playbook_executions"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    playbook_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("incident_playbooks.id"), nullable=False
    )
    incident_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("incidents.id"), nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50), default="in_progress"
    )  # in_progress, completed, aborted
    current_step: Mapped[int] = mapped_column(Integer, default=0)
    step_statuses: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # [{step_index, status, completed_by, completed_at, notes}]

    playbook = relationship("IncidentPlaybook", lazy="selectin")
    incident = relationship("Incident", lazy="selectin")
