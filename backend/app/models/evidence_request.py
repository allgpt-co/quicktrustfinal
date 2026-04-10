import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class EvidenceRequest(BaseModel):
    __tablename__ = "evidence_requests"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    audit_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("audits.id"), nullable=True
    )
    control_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("controls.id"), nullable=True
    )
    requested_by: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=False
    )
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    evidence_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("evidence.id"), nullable=True
    )

    organization = relationship("Organization", lazy="selectin")
    requester = relationship("User", foreign_keys=[requested_by], lazy="selectin")
    assignee = relationship("User", foreign_keys=[assigned_to], lazy="selectin")
