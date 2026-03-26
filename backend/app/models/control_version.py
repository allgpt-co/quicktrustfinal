"""Control version history — tracks every change to a control."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class ControlVersion(BaseModel):
    __tablename__ = "control_versions"

    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(GUID(), ForeignKey("users.id"))
    change_reason: Mapped[str | None] = mapped_column(String(500))

    # Snapshot of the control at this version
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    implementation_details: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50))
    effectiveness: Mapped[str | None] = mapped_column(String(50))
    test_procedure: Mapped[str | None] = mapped_column(Text)

    # What changed (diff)
    changes: Mapped[dict | None] = mapped_column(JSONType())
    # e.g., {"status": {"old": "draft", "new": "implemented"}, "description": {"old": "...", "new": "..."}}

    control = relationship("Control", lazy="selectin")
    changed_by_user = relationship("User", foreign_keys=[changed_by], lazy="selectin")
