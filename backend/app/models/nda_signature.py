import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel, GUID, JSONType


class NdaSignature(BaseModel):
    __tablename__ = "nda_signatures"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    signer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    signer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    signer_company: Mapped[str | None] = mapped_column(String(255))
    signed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ip_address: Mapped[str | None] = mapped_column(String(45))
    document_ids_accessed: Mapped[dict | None] = mapped_column(
        JSONType(), default=list
    )

    organization = relationship("Organization", lazy="selectin")
