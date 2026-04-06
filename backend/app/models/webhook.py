"""Webhook endpoint and delivery models for outbound event webhooks."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel, GUID, JSONType


class WebhookEndpoint(BaseModel):
    __tablename__ = "webhook_endpoints"

    org_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("organizations.id"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    secret: Mapped[str | None] = mapped_column(
        String(255)
    )  # for HMAC signature verification
    events: Mapped[list | None] = mapped_column(
        JSONType(), default=list
    )  # ["incident.created", "control.status_changed"]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_triggered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    failure_count: Mapped[int] = mapped_column(Integer, default=0)


class WebhookDelivery(BaseModel):
    __tablename__ = "webhook_deliveries"

    webhook_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("webhook_endpoints.id"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSONType())
    status_code: Mapped[int | None] = mapped_column(Integer)
    response_body: Mapped[str | None] = mapped_column(Text)
    success: Mapped[bool] = mapped_column(Boolean, default=False)
