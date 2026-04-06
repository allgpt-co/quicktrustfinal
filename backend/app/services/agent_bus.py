"""Redis Pub/Sub for inter-agent communication."""

import json
import logging

from app.config import get_settings

logger = logging.getLogger(__name__)

AGENT_CHANNELS: dict[str, list[str]] = {
    "scan_complete": ["risk_assessment", "evidence_generation"],
    "risk_assessed": ["remediation"],
    "controls_generated": ["evidence_generation"],
    "evidence_collected": ["monitoring_daemon"],
}


async def publish_agent_event(event_type: str, payload: dict) -> None:
    """Publish an event to Redis for other agents to consume."""
    import redis.asyncio as aioredis

    settings = get_settings()
    try:
        r = aioredis.from_url(settings.REDIS_URL)
        message = json.dumps({"event": event_type, "payload": payload}, default=str)
        await r.publish(f"agent:{event_type}", message)
        logger.info("Published agent event: %s", event_type)
        await r.aclose()
    except Exception as e:
        logger.warning("Failed to publish agent event: %s", e)


async def start_agent_subscriber() -> None:
    """Start background task that listens for agent events and triggers follow-up agents."""
    import redis.asyncio as aioredis

    settings = get_settings()
    try:
        r = aioredis.from_url(settings.REDIS_URL)
        pubsub = r.pubsub()
        channels = [f"agent:{ch}" for ch in AGENT_CHANNELS]
        await pubsub.subscribe(*channels)
        logger.info(
            "Agent subscriber started, listening on %d channels", len(channels)
        )

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            channel = (
                message["channel"].decode()
                if isinstance(message["channel"], bytes)
                else message["channel"]
            )
            event_type = channel.replace("agent:", "")
            data = json.loads(message["data"])
            downstream = AGENT_CHANNELS.get(event_type, [])
            logger.info(
                "Agent event received: %s -> would trigger: %s",
                event_type,
                downstream,
            )
    except Exception as e:
        logger.warning("Agent subscriber error: %s", e)
