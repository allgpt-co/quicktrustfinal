"""Control dependencies — define which controls depend on others."""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID


class ControlDependency(BaseModel):
    __tablename__ = "control_dependencies"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    control_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    depends_on_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("controls.id", ondelete="CASCADE"), nullable=False, index=True
    )
    dependency_type: Mapped[str] = mapped_column(String(50), default="requires")
    # requires, enhances, conflicts
    notes: Mapped[str | None] = mapped_column(String(500))

    control = relationship("Control", foreign_keys=[control_id], lazy="selectin")
    depends_on = relationship("Control", foreign_keys=[depends_on_id], lazy="selectin")
