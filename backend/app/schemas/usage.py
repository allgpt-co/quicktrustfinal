from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UsageCounterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    kind: str
    period_start: datetime
    period_end: datetime
    period_source: str
    event_count: int
    quantity: int
    known_prompt_tokens: int
    known_completion_tokens: int
    known_cost_micros: int
    unknown_token_events: int
    unpriced_events: int


class UsageResponse(BaseModel):
    org_id: UUID
    counters: list[UsageCounterResponse]
    next_offset: int | None
    pending_ai_calls: int
    unprojected_ai_calls: int
    excluded_mock_events: int
    instrumented_kinds: list[str]
    coverage: str
    enforcement_enabled: bool
