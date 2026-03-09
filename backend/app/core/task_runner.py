import asyncio
import logging
from typing import Coroutine
from uuid import UUID

logger = logging.getLogger(__name__)

# Track active tasks per org for concurrency control
_active_tasks: dict[str, int] = {}
MAX_CONCURRENT_TASKS_PER_ORG = 5

# IMPORTANT: Keep strong references to background tasks to prevent GC before
# they complete.  See https://docs.python.org/3/library/asyncio-task.html#creating-tasks
_background_tasks: set[asyncio.Task] = set()


async def run_safe_task(
    coro: Coroutine,
    agent_run_id: UUID | None = None,
    org_id: UUID | None = None,
):
    """Run an async task with error handling, logging, and concurrency limits."""
    # Yield control back to the event loop so the originating request handler
    # can finish and release its DB session/connection before we open a new one.
    # Without this, the background task races with the request's session cleanup
    # and triggers "concurrent operations are not permitted" from SQLAlchemy.
    await asyncio.sleep(0.1)

    org_key = str(org_id) if org_id else "global"

    if _active_tasks.get(org_key, 0) >= MAX_CONCURRENT_TASKS_PER_ORG:
        logger.warning("Concurrency limit reached for org %s", org_key)
        if agent_run_id:
            await _mark_agent_run_failed(agent_run_id, "Concurrency limit exceeded")
        return

    _active_tasks[org_key] = _active_tasks.get(org_key, 0) + 1
    try:
        await coro
    except Exception as e:
        logger.error("Background task failed: %s", e, exc_info=True)
        if agent_run_id:
            await _mark_agent_run_failed(agent_run_id, str(e))
    finally:
        _active_tasks[org_key] = max(0, _active_tasks.get(org_key, 0) - 1)


async def _mark_agent_run_failed(agent_run_id: UUID, error: str):
    try:
        from app.core.database import bg_async_session
        from app.models.agent_run import AgentRun
        from sqlalchemy import select

        async with bg_async_session() as db:
            result = await db.execute(
                select(AgentRun).where(AgentRun.id == agent_run_id)
            )
            run = result.scalar_one_or_none()
            if run:
                run.status = "failed"
                run.error_message = error[:2000]
                await db.commit()
    except Exception as e:
        logger.error("Failed to mark agent run as failed: %s", e)


def _task_done(task: asyncio.Task) -> None:
    """Remove completed task from the background set and log errors."""
    _background_tasks.discard(task)
    if task.cancelled():
        logger.debug("Background task was cancelled")
    elif task.exception():
        logger.error("Background task raised: %s", task.exception())


def create_safe_task(
    coro: Coroutine,
    agent_run_id: UUID | None = None,
    org_id: UUID | None = None,
):
    """Create a background task with proper error handling."""
    task = asyncio.create_task(run_safe_task(coro, agent_run_id, org_id))
    _background_tasks.add(task)
    task.add_done_callback(_task_done)
    return task
