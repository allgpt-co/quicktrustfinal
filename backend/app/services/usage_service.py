"""Transaction-owned usage writes: callers commit the action, receipt and totals together.

There is intentionally no client-facing usage-write endpoint. Quantities and keys
must come from trusted server actions, never submitted customer usage claims.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from app.core.exceptions import NotFoundError
from app.models.ai_usage import AiUsageEvent
from app.models.billing import Subscription
from app.models.organization import Organization
from app.models.usage import KINDS, PERIOD_SOURCES, UsageCounter, UsageEvent


class UsageConflictError(ValueError):
    """An idempotency key was reused for different consumption."""


def utc(value):
    # ORM SQLite test timestamps are naive; persisted values are always normalized to UTC.
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


@dataclass(frozen=True)
class UsagePeriod:
    start: datetime
    end: datetime
    source: str


def calendar_period(at, *, legacy=False):
    at = utc(at)
    start = at.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(year=start.year + 1, month=1) if start.month == 12 else start.replace(month=start.month + 1)
    return UsagePeriod(start, end, "legacy_calendar_month" if legacy else "calendar_month")


async def resolve_period(db, org_id, at):
    at = utc(at)
    subscription = await db.scalar(select(Subscription).where(Subscription.org_id == org_id))
    if subscription and utc(subscription.current_period_start) <= at < utc(subscription.current_period_end):
        # Meter even suspended customers if a current route still performs work.
        return UsagePeriod(utc(subscription.current_period_start), utc(subscription.current_period_end), "subscription")
    return calendar_period(at)


def ai_period(event):
    if event.usage_period_start is not None and event.usage_period_end is not None and event.usage_period_source:
        return UsagePeriod(utc(event.usage_period_start), utc(event.usage_period_end), event.usage_period_source)
    # Pre-QT009 calls lack a contract-period snapshot. Never guess from today's subscription.
    return calendar_period(event.created_at, legacy=True)


def _insert(db, table):
    dialect = db.get_bind().dialect.name
    if dialect == "postgresql":
        return pg_insert(table)
    if dialect == "sqlite":
        return sqlite_insert(table)
    raise RuntimeError("Atomic usage accounting requires PostgreSQL or SQLite")


def _integer(name, value, *, nullable=False, signed=False):
    if value is None and nullable:
        return
    minimum = -(2**63) if signed else 0
    if isinstance(value, bool) or not isinstance(value, int) or not minimum <= value <= 2**63 - 1:
        raise ValueError(f"{name} must be an integer in the supported range")


async def append_event(db, *, org_id, kind, idempotency_key, source_type, source_id, occurred_at,
                       quantity=1, user_id=None, prompt_tokens=None, completion_tokens=None,
                       cost_micros=None, is_mock=False, period=None):
    """Return True for a new receipt, False for an identical retry. Never commit here.

    Atomic ON CONFLICT increments prevent lost updates across processes. The
    unique receipt key gates the increment, so retries cannot increment twice.
    """
    if kind not in KINDS:
        raise ValueError("Unsupported usage kind")
    for name, value, maximum in (("idempotency_key", idempotency_key, 200), ("source_type", source_type, 40), ("source_id", source_id, 200)):
        if not isinstance(value, str) or not value or len(value) > maximum:
            raise ValueError(f"Invalid {name}")
    if not isinstance(is_mock, bool):
        raise ValueError("is_mock must be a boolean")
    _integer("quantity", quantity, signed=kind == "STORAGE_BYTES")
    for name, value in (("prompt_tokens", prompt_tokens), ("completion_tokens", completion_tokens), ("cost_micros", cost_micros)):
        _integer(name, value, nullable=True)
    at = utc(occurred_at)
    period = period or await resolve_period(db, org_id, at)
    period = UsagePeriod(utc(period.start), utc(period.end), period.source)
    if period.source not in PERIOD_SOURCES or not period.start <= at < period.end:
        raise ValueError("Usage timestamp must belong to its period")
    financial = dict(quantity=quantity, prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
                     cost_micros=cost_micros, is_mock=is_mock, source_type=source_type, source_id=source_id)
    bucket = dict(org_id=org_id, kind=kind, period_start=period.start, period_end=period.end, period_source=period.source)
    statement = _insert(db, UsageEvent).values(id=uuid4(), idempotency_key=idempotency_key,
        occurred_at=at, user_id=user_id, **bucket, **financial).on_conflict_do_nothing(
            index_elements=["org_id", "kind", "idempotency_key"]).returning(UsageEvent.id)
    inserted = (await db.execute(statement)).scalar_one_or_none()
    if inserted is None:
        existing = await db.scalar(select(UsageEvent).where(
            UsageEvent.org_id == org_id, UsageEvent.kind == kind, UsageEvent.idempotency_key == idempotency_key))
        if existing is None or any(getattr(existing, key) != value for key, value in financial.items()):
            raise UsageConflictError("Usage key already records different consumption")
        # Original actor and period win: a retry must not move an event to a new period.
        return False
    if is_mock:
        return True  # retain the receipt, exclude simulated activity from consumption totals
    increments = dict(event_count=1, quantity=quantity, known_prompt_tokens=prompt_tokens or 0,
                      known_completion_tokens=completion_tokens or 0, known_cost_micros=cost_micros or 0,
                      unknown_token_events=int((kind == "LLM_COMPLETION" and (prompt_tokens is None or completion_tokens is None))
                                               or (kind == "EMBEDDING" and prompt_tokens is None)),
                      unpriced_events=int(cost_micros is None))
    statement = _insert(db, UsageCounter).values(id=uuid4(), **bucket, **increments)
    await db.execute(statement.on_conflict_do_update(
        index_elements=["org_id", "kind", "period_start", "period_end", "period_source"],
        set_={**{key: getattr(UsageCounter, key) + getattr(statement.excluded, key) for key in increments},
              "updated_at": datetime.now(timezone.utc)}))
    return True


async def project_ai_call(db, event, *, values=None):
    """One accounting receipt per existing provider ledger row; cost is counted here only."""
    data = values or {key: getattr(event, key) for key in ("status", "prompt_tokens", "completion_tokens", "cost_micros")}
    if data["status"] == "started":
        return False
    return await append_event(db, org_id=event.org_id, kind="LLM_COMPLETION",
        idempotency_key=str(event.id), source_type="ai_call", source_id=str(event.id),
        user_id=event.user_id, occurred_at=event.created_at, period=ai_period(event),
        prompt_tokens=data["prompt_tokens"], completion_tokens=data["completion_tokens"],
        cost_micros=data["cost_micros"], is_mock=data["status"] == "mock")


def unprojected_ai_query(org_id):
    recorded = select(UsageEvent.id).where(UsageEvent.org_id == AiUsageEvent.org_id,
        UsageEvent.kind == "LLM_COMPLETION", UsageEvent.idempotency_key == AiUsageEvent.id).exists()
    return select(AiUsageEvent).where(AiUsageEvent.org_id == org_id,
        AiUsageEvent.status.in_(["reported", "unknown", "mock"]), ~recorded)


async def backfill_ai_calls(db, org_id, *, limit=100):
    """Bounded, resumable projection. Caller commits the batch; no historical guesses."""
    if not 1 <= limit <= 1000:
        raise ValueError("limit must be between 1 and 1000")
    events = list((await db.scalars(unprojected_ai_query(org_id).order_by(AiUsageEvent.created_at, AiUsageEvent.id).limit(limit))).all())
    for event in events:
        await project_ai_call(db, event)
    return len(events)


async def get_usage(db, org_id, *, offset=0, limit=50):
    org = await db.scalar(select(Organization.id).where(Organization.id == org_id, Organization.deleted_at.is_(None)))
    if org is None:
        raise NotFoundError("Organization not found")
    query = select(UsageCounter).where(UsageCounter.org_id == org_id).order_by(
        UsageCounter.period_start.desc(), UsageCounter.period_end.desc(), UsageCounter.period_source, UsageCounter.kind)
    counters = list((await db.scalars(query.offset(offset).limit(limit + 1))).all())
    pending = await db.scalar(select(func.count()).select_from(AiUsageEvent).where(
        AiUsageEvent.org_id == org_id, AiUsageEvent.status == "started"))
    unprojected = await db.scalar(select(func.count()).select_from(unprojected_ai_query(org_id).subquery()))
    mock_events = await db.scalar(select(func.count()).select_from(UsageEvent).where(
        UsageEvent.org_id == org_id, UsageEvent.is_mock.is_(True)))
    return dict(org_id=org_id, counters=counters[:limit], next_offset=offset + limit if len(counters) > limit else None,
                pending_ai_calls=pending, unprojected_ai_calls=unprojected, excluded_mock_events=mock_events,
                instrumented_kinds=["LLM_COMPLETION", "QUESTION_ANSWERED", "QUESTION_MATCHED", "QUESTIONNAIRE_PROCESSED"],
                coverage="Questionnaire Auto-fill only. Historical answers/completions are not reconstructed; legacy AI calls require backfill.",
                enforcement_enabled=False)
