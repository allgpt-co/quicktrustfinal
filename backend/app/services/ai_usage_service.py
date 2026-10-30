"""Meter Auto-fill independently of answer persistence, using provider token counts."""
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

from app.config import get_settings
from app.models.ai_usage import AiUsageEvent


class UsageRecordingError(RuntimeError):
    pass


def _rate(value):
    try:
        rate = Decimal(str(value))
        # Zero is the existing configuration's unset-price default, not a free model.
        if not rate.is_finite() or rate <= 0:
            return None
        # Match the database snapshot precision before using the rate in arithmetic.
        rate = rate.quantize(Decimal("0.00000001"), rounding=ROUND_HALF_UP)
        return rate if rate > 0 else None
    except (InvalidOperation, ValueError):
        return None


def _model(value):
    return str(value or "").removeprefix("bedrock/")


def estimate_cost_micros(prompt_tokens, completion_tokens, input_rate, output_rate):
    """USD per million tokens * tokens = micro-USD; round only the final sum."""
    with localcontext() as context:
        context.prec = 50
        return int((Decimal(prompt_tokens) * input_rate + Decimal(completion_tokens) * output_rate)
                   .quantize(Decimal("1"), rounding=ROUND_HALF_UP))


async def start_call(db, *, org_id, questionnaire_id, user_id=None, job_id=None, batch_index=0):
    settings = get_settings()
    event = AiUsageEvent(
        org_id=org_id, questionnaire_id=questionnaire_id, user_id=user_id,
        job_id=job_id, batch_index=batch_index,
        model=_model(settings.BEDROCK_MODEL_ID) if settings.BEDROCK_ENABLED else "mock",
        input_rate_per_million=_rate(settings.BEDROCK_INPUT_COST_PER_MILLION),
        output_rate_per_million=_rate(settings.BEDROCK_OUTPUT_COST_PER_MILLION),
        status="started",
    )
    try:
        db.add(event)
        await db.commit()  # must succeed before incurring provider spend
    except SQLAlchemyError as exc:
        await db.rollback()
        raise UsageRecordingError("Could not start AI usage record") from exc
    return event


async def finish_call(db, event, usage=None):
    """Idempotently finalize one call. Unknown usage/cost is NULL, never invented zero."""
    usage = usage or {}
    model = _model(usage.get("model")) or event.model
    prompt, completion = usage.get("prompt_tokens"), usage.get("completion_tokens")
    known = usage.get("usage_available", True) and all(
        isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in (prompt, completion)
    )
    mock = model == "mock" and bool(usage)
    cost = None
    if mock:
        prompt, completion, cost = 0, 0, 0
    elif (known and _model(model) == _model(event.model)
          and event.input_rate_per_million is not None
          and event.output_rate_per_million is not None):
        cost = estimate_cost_micros(prompt, completion, event.input_rate_per_million, event.output_rate_per_million)
    values = dict(status="mock" if mock else "reported" if known else "unknown",
                  model=model, prompt_tokens=prompt if known or mock else None,
                  completion_tokens=completion if known or mock else None,
                  cost_micros=cost, recorded_at=datetime.now(timezone.utc))
    try:
        # Repeated callbacks or finalization retries cannot add consumption twice.
        await db.execute(update(AiUsageEvent).where(
            AiUsageEvent.id == event.id, AiUsageEvent.org_id == event.org_id,
            AiUsageEvent.status == "started",
        ).values(**values).execution_options(synchronize_session=False))
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise UsageRecordingError("Could not save AI usage record") from exc
