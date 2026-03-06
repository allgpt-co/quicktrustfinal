import redis.asyncio as redis
from app.config import get_settings

_redis = None


async def get_redis():
    global _redis
    if _redis is None:
        settings = get_settings()
        _redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis


async def blacklist_token(jti: str, expires_in: int):
    """Add a token's JTI to the blacklist until it naturally expires."""
    r = await get_redis()
    await r.setex(f"blacklist:{jti}", expires_in, "1")


async def is_token_blacklisted(jti: str) -> bool:
    """Check if a token has been revoked."""
    r = await get_redis()
    return await r.exists(f"blacklist:{jti}") > 0
