"""Evidence version tracking -- snapshots every change to an evidence item."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class EvidenceVersion(BaseModel):
    __tablename__ = "evidence_versions"

    evidence_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("evidence.id", ondelete="CASCADE"), nullable=False, index=True
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    collection_method: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text)
    file_url: Mapped[str | None] = mapped_column(String(1000))
    file_hash: Mapped[str | None] = mapped_column(String(128))
    change_reason: Mapped[str | None] = mapped_column(String(500))
    changes: Mapped[dict | None] = mapped_column(JSONType())  # {"field": {"old": ..., "new": ...}}
    changed_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id")
    )

    evidence = relationship("Evidence", lazy="selectin")
    changed_by_user = relationship("User", foreign_keys=[changed_by], lazy="selectin")
