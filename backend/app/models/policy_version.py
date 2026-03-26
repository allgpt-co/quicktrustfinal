"""Policy version history — stores full text snapshots for diff comparison."""

import uuid

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class PolicyVersion(BaseModel):
    __tablename__ = "policy_versions"

    policy_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("policies.id", ondelete="CASCADE"), nullable=False, index=True
    )
    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    changed_by: Mapped[uuid.UUID | None] = mapped_column(GUID(), ForeignKey("users.id"))
    change_summary: Mapped[str | None] = mapped_column(String(500))
    status_at_version: Mapped[str | None] = mapped_column(String(50))
    changes: Mapped[dict | None] = mapped_column(JSONType())

    policy = relationship("Policy", lazy="selectin")
    changed_by_user = relationship("User", foreign_keys=[changed_by], lazy="selectin")
