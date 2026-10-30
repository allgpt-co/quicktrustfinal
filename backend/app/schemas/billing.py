from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StrictBool, model_validator


Limit = Annotated[int, Field(strict=True, ge=0, le=2**63 - 1)] | None
FeatureKey = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")]
Features = Annotated[dict[FeatureKey, StrictBool], Field(max_length=100)]
Status = Literal["trialing", "active", "past_due", "suspended", "canceled"]


class Limits(BaseModel):
    model_config = ConfigDict(extra="forbid")
    seats: Limit = None
    ai_answers_per_period: Limit = None
    questionnaires_per_period: Limit = None
    documents: Limit = None
    storage_bytes: Limit = None


class PlanCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    code: str = Field(min_length=1, max_length=80, pattern=r"^[a-z][a-z0-9_\-]*$")
    name: str = Field(min_length=1, max_length=255)
    is_active: StrictBool = True
    limits: Limits = Field(default_factory=Limits)
    features: Features = Field(default_factory=dict)


class PlanResponse(PlanCreate):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    created_at: datetime


class SubscriptionPut(BaseModel):
    """Full replacement; version 0 creates, current version updates. Dates require timezone."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    expected_version: Annotated[int, Field(strict=True, ge=0)]
    plan_id: UUID
    status: Status
    source: Literal["manual"] = "manual"
    billing_interval: Literal["month", "year"]
    current_period_start: AwareDatetime
    current_period_end: AwareDatetime
    trial_ends_at: AwareDatetime | None = None
    contract_ref: str | None = Field(default=None, max_length=255)
    limit_overrides: Limits = Field(default_factory=Limits)
    feature_overrides: Features = Field(default_factory=dict)

    @model_validator(mode="after")
    def valid_period(self):
        if self.current_period_end <= self.current_period_start:
            raise ValueError("Period end must be after period start")
        if self.status == "trialing" and self.trial_ends_at is None:
            raise ValueError("Trial subscriptions require trial_ends_at")
        if self.trial_ends_at is not None and not self.current_period_start < self.trial_ends_at <= self.current_period_end:
            raise ValueError("Trial end must fall within the subscription period")
        return self


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    org_id: UUID
    plan_id: UUID
    status: Status
    source: Literal["manual"]
    billing_interval: Literal["month", "year"]
    current_period_start: datetime
    current_period_end: datetime
    trial_ends_at: datetime | None
    canceled_at: datetime | None
    contract_ref: str | None
    # Preserve sparse overrides, including explicit null (no configured cap).
    limit_overrides: dict[str, Limit]
    feature_overrides: Features
    version: int
    created_at: datetime
    updated_at: datetime


class EntitlementResponse(BaseModel):
    org_id: UUID
    configured: bool
    access_allowed: bool
    reason: str
    plan_code: str | None
    subscription_status: Status | None
    limits: Limits
    features: Features
    enforcement_enabled: bool = False


class BillingResponse(BaseModel):
    subscription: SubscriptionResponse | None
    entitlements: EntitlementResponse
