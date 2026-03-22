"""Durable workflow engine — wraps task runner with DB persistence for crash recovery."""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workflow import WorkflowExecution

logger = logging.getLogger(__name__)


async def create_workflow(
    db: AsyncSession,
    org_id: UUID,
    workflow_type: str,
    reference_id: UUID | None = None,
    input_data: dict | None = None,
    total_steps: int = 1,
    triggered_by: UUID | None = None,
) -> WorkflowExecution:
    """Create a new workflow execution record."""
    wf = WorkflowExecution(
        org_id=org_id,
        workflow_type=workflow_type,
        reference_id=reference_id,
        status="pending",
        current_step=0,
        total_steps=total_steps,
        input_data=input_data,
        triggered_by=triggered_by,
    )
    db.add(wf)
    await db.commit()
    await db.refresh(wf)
    return wf


async def start_workflow(db: AsyncSession, workflow_id: UUID) -> WorkflowExecution:
    """Mark a workflow as running."""
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.id == workflow_id)
    )
    wf = result.scalar_one_or_none()
    if wf:
        wf.status = "running"
        wf.started_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(wf)
    return wf


async def advance_step(
    db: AsyncSession, workflow_id: UUID, step_name: str, step_number: int | None = None,
) -> WorkflowExecution:
    """Advance workflow to the next step."""
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.id == workflow_id)
    )
    wf = result.scalar_one_or_none()
    if wf:
        wf.current_step = step_number if step_number is not None else wf.current_step + 1
        wf.step_name = step_name
        await db.commit()
        await db.refresh(wf)
    return wf


async def complete_workflow(
    db: AsyncSession, workflow_id: UUID, output_data: dict | None = None,
) -> WorkflowExecution:
    """Mark a workflow as completed."""
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.id == workflow_id)
    )
    wf = result.scalar_one_or_none()
    if wf:
        wf.status = "completed"
        wf.completed_at = datetime.now(timezone.utc)
        wf.output_data = output_data
        wf.current_step = wf.total_steps
        await db.commit()
        await db.refresh(wf)
    return wf


async def fail_workflow(
    db: AsyncSession, workflow_id: UUID, error: str,
) -> WorkflowExecution:
    """Mark a workflow as failed."""
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.id == workflow_id)
    )
    wf = result.scalar_one_or_none()
    if wf:
        wf.status = "failed"
        wf.error_message = error[:2000]
        wf.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(wf)
    return wf


async def get_workflow(db: AsyncSession, workflow_id: UUID) -> WorkflowExecution | None:
    result = await db.execute(
        select(WorkflowExecution).where(WorkflowExecution.id == workflow_id)
    )
    return result.scalar_one_or_none()


async def list_workflows(
    db: AsyncSession, org_id: UUID,
    workflow_type: str | None = None,
    status: str | None = None,
    page: int = 1, page_size: int = 50,
) -> tuple[list[WorkflowExecution], int]:
    """List workflows with optional filters."""
    from sqlalchemy import func

    base_q = select(WorkflowExecution).where(WorkflowExecution.org_id == org_id)
    count_q = select(func.count()).select_from(WorkflowExecution).where(
        WorkflowExecution.org_id == org_id
    )

    if workflow_type:
        base_q = base_q.where(WorkflowExecution.workflow_type == workflow_type)
        count_q = count_q.where(WorkflowExecution.workflow_type == workflow_type)
    if status:
        base_q = base_q.where(WorkflowExecution.status == status)
        count_q = count_q.where(WorkflowExecution.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        WorkflowExecution.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def recover_stale_workflows(db: AsyncSession, timeout_minutes: int = 30) -> int:
    """Find workflows stuck in 'running' state and mark them for retry or failure.

    Called on server startup to recover from crashes.
    """
    from datetime import timedelta

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=timeout_minutes)

    result = await db.execute(
        select(WorkflowExecution).where(
            WorkflowExecution.status == "running",
            WorkflowExecution.started_at < cutoff,
        )
    )
    stale = list(result.scalars().all())
    recovered = 0

    for wf in stale:
        if wf.retry_count < wf.max_retries:
            wf.status = "retrying"
            wf.retry_count += 1
            logger.info(
                "Recovering stale workflow %s (type=%s, retry %d/%d)",
                wf.id, wf.workflow_type, wf.retry_count, wf.max_retries,
            )
        else:
            wf.status = "failed"
            wf.error_message = f"Workflow timed out after {timeout_minutes} minutes and exhausted {wf.max_retries} retries"
            wf.completed_at = datetime.now(timezone.utc)
            logger.warning("Failing stale workflow %s after max retries", wf.id)
        recovered += 1

    if recovered:
        await db.commit()

    return recovered
