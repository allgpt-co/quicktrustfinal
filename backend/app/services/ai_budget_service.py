"""AI Budget & Token tracking via Redis.

Tracks per-org monthly token usage and enforces spending limits.
"""

import logging
from datetime import datetime, timezone
from uuid import UUID

logger = logging.getLogger(__name__)

# Default limits (can be overridden per org via settings)
DEFAULT_MONTHLY_TOKEN_LIMIT = 1_000_000  # 1M tokens
DEFAULT_MONTHLY_COST_LIMIT = 50.0  # $50 USD

# Approximate cost per 1K tokens (GPT-4o-mini pricing)
COST_PER_1K_INPUT = 0.00015
COST_PER_1K_OUTPUT = 0.0006


def _month_key(org_id: str) -> str:
    """Redis key for current month's usage."""
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    return f"ai_budget:{org_id}:{month}"


async def record_usage(org_id: str, tokens: int, cost_usd: float = 0.0) -> None:
    """Record token usage for an org in the current month."""
    try:
        from app.core.token_blacklist import get_redis
        r = await get_redis()
        key = _month_key(org_id)
        pipe = r.pipeline()
        pipe.hincrby(key, "tokens", tokens)
        pipe.hincrbyfloat(key, "cost", cost_usd)
        pipe.hincrby(key, "calls", 1)
        pipe.expire(key, 35 * 86400)  # expire after 35 days
        await pipe.execute()
    except Exception as exc:
        logger.warning("Failed to record AI usage: %s", exc)


async def get_usage(org_id: str) -> dict:
    """Get current month's AI usage for an org."""
    try:
        from app.core.token_blacklist import get_redis
        r = await get_redis()
        key = _month_key(org_id)
        data = await r.hgetall(key)
        tokens = int(data.get("tokens", 0))
        cost = float(data.get("cost", 0.0))
        calls = int(data.get("calls", 0))
        month = datetime.now(timezone.utc).strftime("%Y-%m")

        return {
            "org_id": org_id,
            "month": month,
            "tokens_used": tokens,
            "tokens_limit": DEFAULT_MONTHLY_TOKEN_LIMIT,
            "cost_usd": round(cost, 4),
            "cost_limit_usd": DEFAULT_MONTHLY_COST_LIMIT,
            "usage_percent": round((tokens / DEFAULT_MONTHLY_TOKEN_LIMIT) * 100, 1) if DEFAULT_MONTHLY_TOKEN_LIMIT > 0 else 0,
            "budget_exceeded": tokens >= DEFAULT_MONTHLY_TOKEN_LIMIT or cost >= DEFAULT_MONTHLY_COST_LIMIT,
            "calls": calls,
        }
    except Exception as exc:
        logger.warning("Failed to get AI usage: %s", exc)
        return {
            "org_id": org_id,
            "month": datetime.now(timezone.utc).strftime("%Y-%m"),
            "tokens_used": 0,
            "tokens_limit": DEFAULT_MONTHLY_TOKEN_LIMIT,
            "cost_usd": 0.0,
            "cost_limit_usd": DEFAULT_MONTHLY_COST_LIMIT,
            "usage_percent": 0.0,
            "budget_exceeded": False,
            "calls": 0,
        }


async def check_budget(org_id: str) -> tuple[bool, str]:
    """Check if org has remaining AI budget.

    Returns (allowed, reason).
    """
    usage = await get_usage(org_id)
    if usage["tokens_used"] >= usage["tokens_limit"]:
        return False, f"Monthly token limit exceeded ({usage['tokens_used']:,}/{usage['tokens_limit']:,})"
    if usage["cost_usd"] >= usage["cost_limit_usd"]:
        return False, f"Monthly cost limit exceeded (${usage['cost_usd']:.2f}/${usage['cost_limit_usd']:.2f})"
    return True, "OK"


def estimate_cost(tokens: int) -> float:
    """Rough cost estimate for a given token count (assumes 50/50 input/output split)."""
    input_tokens = tokens // 2
    output_tokens = tokens - input_tokens
    return round((input_tokens / 1000) * COST_PER_1K_INPUT + (output_tokens / 1000) * COST_PER_1K_OUTPUT, 6)
