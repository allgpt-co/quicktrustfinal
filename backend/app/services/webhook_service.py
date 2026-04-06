"""Webhook service — dispatch outbound events to registered endpoints."""

import hashlib
import hmac
import json
import logging
from datetime import datetime, timezone
from uuid import UUID

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.task_runner import create_safe_task
from app.models.webhook import WebhookDelivery, WebhookEndpoint

logger = logging.getLogger(__name__)

MAX_FAILURE_COUNT = 10  # disable webhook after this many consecutive failures
DELIVERY_TIMEOUT_SECONDS = 10


def _compute_signature(secret: str, payload_bytes: bytes) -> str:
    """Compute HMAC-SHA256 signature for webhook payload verification."""
    return hmac.new(
        secret.encode("utf-8"),
        payload_bytes,
        hashlib.sha256,
    ).hexdigest()


async def dispatch_event(
    db: AsyncSession,
    org_id: UUID,
    event_type: str,
    payload: dict,
) -> int:
    """Send an event to all active webhooks subscribed to that event type.

    Returns the number of webhooks that were dispatched to.
    """
    result = await db.execute(
        select(WebhookEndpoint).where(
            WebhookEndpoint.org_id == org_id,
            WebhookEndpoint.is_active.is_(True),
        )
    )
    webhooks = list(result.scalars().all())

    dispatched = 0
    for webhook in webhooks:
        subscribed_events = webhook.events or []
        # Empty events list means subscribe to all events
        if subscribed_events and event_type not in subscribed_events:
            continue

        # Fire-and-forget delivery
        create_safe_task(
            _deliver(db, webhook, event_type, payload),
            org_id=org_id,
        )
        dispatched += 1

    return dispatched


async def _deliver(
    db: AsyncSession,
    webhook: WebhookEndpoint,
    event_type: str,
    payload: dict,
) -> None:
    """Deliver a single webhook event and log the result."""
    from app.core.database import async_session

    payload_bytes = json.dumps(payload, default=str).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "X-QuickTrust-Event": event_type,
    }
    if webhook.secret:
        signature = _compute_signature(webhook.secret, payload_bytes)
        headers["X-QuickTrust-Signature"] = f"sha256={signature}"

    status_code = None
    response_body = None
    success = False

    try:
        async with httpx.AsyncClient(timeout=DELIVERY_TIMEOUT_SECONDS) as client:
            resp = await client.post(
                webhook.url,
                content=payload_bytes,
                headers=headers,
            )
            status_code = resp.status_code
            response_body = resp.text[:2000]
            success = 200 <= resp.status_code < 300
    except Exception as exc:
        response_body = str(exc)[:2000]
        logger.warning(
            "Webhook delivery failed for %s -> %s: %s",
            event_type,
            webhook.url,
            exc,
        )

    # Persist delivery record in a fresh session
    async with async_session() as new_db:
        delivery = WebhookDelivery(
            webhook_id=webhook.id,
            event_type=event_type,
            payload=payload,
            status_code=status_code,
            response_body=response_body,
            success=success,
        )
        new_db.add(delivery)

        # Update webhook metadata
        wh_result = await new_db.execute(
            select(WebhookEndpoint).where(WebhookEndpoint.id == webhook.id)
        )
        wh = wh_result.scalar_one_or_none()
        if wh:
            wh.last_triggered_at = datetime.now(timezone.utc)
            if success:
                wh.failure_count = 0
            else:
                wh.failure_count = (wh.failure_count or 0) + 1
                if wh.failure_count >= MAX_FAILURE_COUNT:
                    wh.is_active = False
                    logger.warning(
                        "Webhook %s disabled after %d consecutive failures",
                        wh.id,
                        wh.failure_count,
                    )

        await new_db.commit()


async def list_webhooks(
    db: AsyncSession, org_id: UUID
) -> list[WebhookEndpoint]:
    """List all webhooks for an organization."""
    result = await db.execute(
        select(WebhookEndpoint)
        .where(WebhookEndpoint.org_id == org_id)
        .order_by(WebhookEndpoint.created_at.desc())
    )
    return list(result.scalars().all())


async def create_webhook(
    db: AsyncSession, org_id: UUID, url: str, secret: str | None, events: list[str]
) -> WebhookEndpoint:
    """Create a new webhook endpoint."""
    webhook = WebhookEndpoint(
        org_id=org_id,
        url=url,
        secret=secret,
        events=events,
        is_active=True,
        failure_count=0,
    )
    db.add(webhook)
    await db.commit()
    await db.refresh(webhook)
    return webhook


async def delete_webhook(
    db: AsyncSession, org_id: UUID, webhook_id: UUID
) -> None:
    """Delete a webhook endpoint."""
    from app.core.exceptions import NotFoundError

    result = await db.execute(
        select(WebhookEndpoint).where(
            WebhookEndpoint.id == webhook_id,
            WebhookEndpoint.org_id == org_id,
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise NotFoundError("Webhook not found")
    await db.delete(webhook)
    await db.commit()


async def list_deliveries(
    db: AsyncSession, org_id: UUID, webhook_id: UUID, limit: int = 50
) -> list[WebhookDelivery]:
    """List recent deliveries for a webhook."""
    from app.core.exceptions import NotFoundError

    # Verify webhook belongs to org
    wh_result = await db.execute(
        select(WebhookEndpoint).where(
            WebhookEndpoint.id == webhook_id,
            WebhookEndpoint.org_id == org_id,
        )
    )
    if not wh_result.scalar_one_or_none():
        raise NotFoundError("Webhook not found")

    result = await db.execute(
        select(WebhookDelivery)
        .where(WebhookDelivery.webhook_id == webhook_id)
        .order_by(WebhookDelivery.created_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())


async def send_test_event(
    db: AsyncSession, org_id: UUID, webhook_id: UUID
) -> dict:
    """Send a test event to a specific webhook."""
    from app.core.exceptions import NotFoundError

    result = await db.execute(
        select(WebhookEndpoint).where(
            WebhookEndpoint.id == webhook_id,
            WebhookEndpoint.org_id == org_id,
        )
    )
    webhook = result.scalar_one_or_none()
    if not webhook:
        raise NotFoundError("Webhook not found")

    test_payload = {
        "event": "webhook.test",
        "org_id": str(org_id),
        "message": "This is a test event from QuickTrust",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    await _deliver(db, webhook, "webhook.test", test_payload)
    return {"message": "Test event dispatched", "url": webhook.url}
