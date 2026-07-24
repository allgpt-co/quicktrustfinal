import logging
import time

import redis.asyncio as redis

from app.config import get_settings

logger = logging.getLogger(__name__)

_redis = None


async def get_redis():
    global _redis
    if _redis is None:
        settings = get_settings()
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def blacklist_token(jti: str, expires_in: int):
    """Add a token's JTI to the blacklist until it naturally expires."""
    try:
        r = await get_redis()
        await r.setex(f"blacklist:{jti}", expires_in, "1")
    except Exception as exc:
        logger.warning("Failed to blacklist token %s: %s", jti[:8], exc)


async def is_token_blacklisted(jti: str) -> bool:
    """Check if a token has been revoked."""
    try:
        r = await get_redis()
        return await r.exists(f"blacklist:{jti}") > 0
    except Exception as exc:
        logger.warning("Redis unavailable for blacklist check: %s", exc)
        return False  # Fail open


async def revoke_all_user_tokens(user_id: str) -> None:
    """Revoke ALL tokens for a user by storing a 'revoked-before' timestamp.

    Any token issued before this timestamp is considered invalid.
    Useful for password changes, account compromise, or admin force-logout.
    """
    try:
        r = await get_redis()
        key = f"user:{user_id}:tokens_revoked_at"
        await r.setex(key, 86400, str(time.time()))
        logger.info("Revoked all tokens for user %s", user_id)
    except Exception as exc:
        logger.warning("Failed to revoke user tokens for %s: %s", user_id, exc)


async def is_user_token_revoked(user_id: str, token_issued_at: float) -> bool:
    """Check if a token was issued before a user-level revocation."""
    try:
        r = await get_redis()
        revoked_at = await r.get(f"user:{user_id}:tokens_revoked_at")
        if not revoked_at:
            return False
        return token_issued_at < float(revoked_at)
    except Exception as exc:
        logger.warning("Failed to check user token revocation: %s", exc)
        return False  # Fail open
