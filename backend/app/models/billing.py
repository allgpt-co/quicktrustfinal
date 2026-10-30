"""Commercial configuration; independent of payment collection and quota enforcement."""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import GUID, JSONType


class Plan(Base):
    __tablename__ = "billing_plans"

    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)
    code: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    limits: Mapped[dict] = mapped_column(JSONType(), nullable=False, default=dict)
    features: Mapped[dict] = mapped_column(JSONType(), nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "billing_subscriptions"
    __table_args__ = (
        CheckConstraint("status IN ('trialing','active','past_due','suspended','canceled')", name="ck_subscription_status"),
        CheckConstraint("source = 'manual'", name="ck_subscription_source"),
        CheckConstraint("billing_interval IN ('month','year')", name="ck_subscription_interval"),
        CheckConstraint("current_period_end > current_period_start", name="ck_subscription_period"),
        CheckConstraint("status != 'trialing' OR trial_ends_at IS NOT NULL", name="ck_subscription_trial"),
        CheckConstraint("version >= 1", name="ck_subscription_version"),
    )

    id: Mapped[UUID] = mapped_column(GUID(), primary_key=True, default=uuid4)
    org_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("organizations.id"), unique=True, nullable=False)
    plan_id: Mapped[UUID] = mapped_column(GUID(), ForeignKey("billing_plans.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="manual")
    billing_interval: Mapped[str] = mapped_column(String(10), nullable=False)
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    current_period_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    trial_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    canceled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    contract_ref: Mapped[str | None] = mapped_column(String(255))
    limit_overrides: Mapped[dict] = mapped_column(JSONType(), nullable=False, default=dict)
    feature_overrides: Mapped[dict] = mapped_column(JSONType(), nullable=False, default=dict)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
