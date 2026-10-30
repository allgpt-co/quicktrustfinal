"""Database-backed auto-fill queue. Each API process runs one bounded worker.

Jobs survive restarts; abandoned running jobs fail after the execution deadline
plus a grace period. Users may retry failures; already saved responses are skipped.
"""
import asyncio
import logging
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.orm import lazyload

from app.core.database import bg_async_session
from app.core.exceptions import NotFoundError
from app.core.request_context import current_org_var
from app.models.questionnaire import Questionnaire
from app.models.workflow import WorkflowExecution
from app.services import questionnaire_service

logger = logging.getLogger(__name__)
JOB_TYPE = "questionnaire_auto_fill"
ACTIVE = ("pending", "running")
JOB_TIMEOUT_SECONDS = 15 * 60
POLL_SECONDS = 2


def job_query(org_id: UUID, questionnaire_id: UUID):
    return select(WorkflowExecution).options(lazyload("*")).where(
        WorkflowExecution.org_id == org_id,
        WorkflowExecution.reference_id == questionnaire_id,
        WorkflowExecution.workflow_type == JOB_TYPE,
    )


async def latest_job(db, org_id, questionnaire_id):
    await questionnaire_service.get_questionnaire(db, org_id, questionnaire_id)
    return (await db.execute(job_query(org_id, questionnaire_id).order_by(
        WorkflowExecution.created_at.desc(), WorkflowExecution.id.desc()
    ).limit(1))).scalar_one_or_none()


async def enqueue(db, org_id, questionnaire_id, user_id):
    # Serializes submissions for the same questionnaire across API processes.
    questionnaire = (await db.execute(select(Questionnaire).options(lazyload("*")).where(
        Questionnaire.id == questionnaire_id, Questionnaire.org_id == org_id,
    ).with_for_update())).scalar_one_or_none()
    if questionnaire is None:
        raise NotFoundError("Questionnaire not found")
    existing = (await db.execute(job_query(org_id, questionnaire_id).where(
        WorkflowExecution.status.in_(ACTIVE)
    ))).scalar_one_or_none()
    if existing:
        await db.commit()
        return existing
    job = WorkflowExecution(
        org_id=org_id, reference_id=questionnaire_id, workflow_type=JOB_TYPE,
        created_at=datetime.now(timezone.utc),
        status="pending", current_step=0, total_steps=len(questionnaire.questions or []),
        step_name="Queued", triggered_by=user_id, max_retries=0,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def claim_next():
    async with bg_async_session() as db:
        now = datetime.now(timezone.utc)
        await db.execute(update(WorkflowExecution).where(
            WorkflowExecution.workflow_type == JOB_TYPE,
            WorkflowExecution.status == "running",
            WorkflowExecution.started_at < now - timedelta(seconds=JOB_TIMEOUT_SECONDS + 60),
        ).values(status="failed", completed_at=now,
                 error_message="Processing was interrupted. Retry Auto-fill to continue."))
        job = (await db.execute(select(WorkflowExecution).options(lazyload("*")).where(
            WorkflowExecution.workflow_type == JOB_TYPE,
            WorkflowExecution.status == "pending",
        ).order_by(WorkflowExecution.created_at).with_for_update(skip_locked=True).limit(1))).scalar_one_or_none()
        if job:
            job.status = "running"
            job.started_at = now
            job.step_name = "Matching existing controls and policies"
        await db.commit()
        return (job.id, job.org_id, job.reference_id) if job else None


async def set_progress(job_id, completed, total):
    async with bg_async_session() as db:
        await db.execute(update(WorkflowExecution).where(
            WorkflowExecution.id == job_id, WorkflowExecution.status == "running",
        ).values(current_step=completed, total_steps=total,
                 step_name="Generating answers"))
        await db.commit()


async def finish(job_id, *, count=None, error=None):
    async with bg_async_session() as db:
        values = dict(status="failed" if error else "completed",
                      completed_at=datetime.now(timezone.utc), error_message=error,
                      step_name="Failed" if error else "Completed")
        if error is None:
            values.update(output_data={"filled_count": count}, current_step=WorkflowExecution.total_steps)
        await db.execute(update(WorkflowExecution).where(
            WorkflowExecution.id == job_id, WorkflowExecution.status == "running",
        ).values(**values))
        await db.commit()


async def execute_job(job_id, org_id, questionnaire_id):
    token = current_org_var.set(str(org_id))
    try:
        async with asyncio.timeout(JOB_TIMEOUT_SECONDS):
            async with bg_async_session() as db:
                job = await db.get(WorkflowExecution, job_id)
                if job is None or job.org_id != org_id or job.reference_id != questionnaire_id:
                    raise ValueError("Auto-fill job context does not match its organization/questionnaire")
                count = await questionnaire_service.auto_fill(
                    db, org_id, questionnaire_id,
                    progress=lambda done, total: set_progress(job_id, done, total),
                    strict_errors=True,
                    usage_user_id=job.triggered_by, usage_job_id=job.id,
                )
        await finish(job_id, count=count)
    except asyncio.CancelledError:
        await finish(job_id, error="Processing was interrupted. Retry Auto-fill to continue.")
        raise
    except Exception:
        logger.exception("Questionnaire auto-fill job %s failed", job_id)
        await finish(job_id, error="Auto-fill could not finish. Saved answers are retained; retry to continue.")

    finally:
        current_org_var.reset(token)


async def worker_loop():
    while True:
        try:
            job = await claim_next()
            if job:
                await execute_job(*job)
                continue
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("Questionnaire queue polling failed")
        await asyncio.sleep(POLL_SECONDS)


async def stop_worker(task):
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
