"""Server-Sent Events (SSE) for real-time updates."""

import asyncio
import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from app.core.dependencies import DB, AnyInternalUser, VerifiedOrgId

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/organizations/{org_id}/events",
    tags=["sse"],
)

# In-memory event bus: org_id -> list of asyncio.Queue
_event_queues: dict[str, list[asyncio.Queue]] = {}


async def publish_event(org_id: str, event_type: str, data: dict) -> None:
    """Publish an event to all SSE subscribers for an org."""
    queues = _event_queues.get(org_id, [])
    message = {"event": event_type, "data": json.dumps(data, default=str)}
    for queue in queues:
        try:
            queue.put_nowait(message)
        except asyncio.QueueFull:
            logger.warning("SSE queue full for org %s, dropping event", org_id)


@router.get("/stream")
async def event_stream(
    org_id: VerifiedOrgId,
    request: Request,
    db: DB,
    current_user: AnyInternalUser,
):
    """SSE endpoint — streams real-time events to connected clients."""
    org_key = str(org_id)
    queue: asyncio.Queue = asyncio.Queue(maxsize=100)

    if org_key not in _event_queues:
        _event_queues[org_key] = []
    _event_queues[org_key].append(queue)

    async def event_generator():
        try:
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                try:
                    message = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield message
                except asyncio.TimeoutError:
                    # Send keepalive ping
                    yield {"event": "ping", "data": "{}"}
        finally:
            # Cleanup on disconnect
            if org_key in _event_queues:
                try:
                    _event_queues[org_key].remove(queue)
                except ValueError:
                    pass
                if not _event_queues[org_key]:
                    del _event_queues[org_key]
            logger.debug("SSE client disconnected for org %s", org_key)

    return EventSourceResponse(event_generator())
