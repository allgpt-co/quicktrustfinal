"""APScheduler integration for periodic monitoring checks.

The scheduler reads all active ``MonitorRule`` rows from the database and
creates APScheduler jobs that invoke ``monitoring_service.run_checks`` on the
configured schedule (hourly / daily / weekly).
"""

from __future__ import annotations

import logging
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

# Mapping from MonitorRule.schedule values to APScheduler trigger kwargs
_SCHEDULE_MAP: dict[str, dict] = {
    "hourly": {"trigger": "interval", "hours": 1},
    "daily": {"trigger": "interval", "hours": 24},
    "weekly": {"trigger": "interval", "weeks": 1},
}


async def start_scheduler() -> None:
    """Start the scheduler and load all active monitoring rules as jobs."""
    try:
        from app.core.database import async_session

        # Recover workflows that were interrupted by a server crash
        async with async_session() as db:
            from app.services import workflow_service
            recovered = await workflow_service.recover_stale_workflows(db)
            if recovered:
                logger.info("Recovered %d stale workflows on startup.", recovered)

        async with async_session() as db:
            await sync_monitoring_rules(db)

        # Nightly data-retention enforcement (GDPR / Fix 10.5)
        scheduler.add_job(
            _run_retention_enforcement,
            trigger="cron",
            hour=2,
            minute=0,
            id="data_retention_enforcement",
            replace_existing=True,
        )

        # Nightly database backup at 1 AM
        scheduler.add_job(
            _run_database_backup,
            trigger="cron",
            hour=1,
            minute=0,
            id="database_backup",
            replace_existing=True,
        )

        # Scheduled evidence collection — check every 5 minutes for due integrations
        scheduler.add_job(
            _run_scheduled_collections,
            trigger="interval",
            minutes=5,
            id="scheduled_evidence_collection",
            replace_existing=True,
        )

        # Evidence freshness + compliance regression checks — every 6 hours
        scheduler.add_job(
            _run_alert_engine,
            trigger="interval",
            hours=6,
            id="alert_engine",
            replace_existing=True,
        )

        # Control test execution — run daily at 3 AM
        scheduler.add_job(
            _run_control_tests,
            trigger="cron",
            hour=3,
            minute=0,
            id="control_test_execution",
            replace_existing=True,
        )

        # Scheduled report delivery — check every hour for due reports
        scheduler.add_job(
            _run_scheduled_reports,
            trigger="interval",
            hours=1,
            id="scheduled_report_delivery",
            replace_existing=True,
        )

        # Daily policy review check at 8 AM — flag overdue annual reviews
        scheduler.add_job(
            _run_policy_review_check,
            trigger="cron",
            hour=8,
            minute=0,
            id="policy_review_check",
            replace_existing=True,
        )

        scheduler.start()
        logger.info("APScheduler started with monitoring, collection, and control test jobs.")
    except Exception as exc:
        logger.warning("Failed to start scheduler: %s. Monitoring jobs will be disabled.", exc)


async def stop_scheduler() -> None:
    """Gracefully shut down the scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")


async def sync_monitoring_rules(db) -> None:
    """Read all active monitoring rules and create/update APScheduler jobs.

    Existing jobs whose rule has been deactivated or deleted are removed.
    """
    from app.models.monitoring import MonitorRule

    result = await db.execute(
        select(MonitorRule).where(MonitorRule.is_active.is_(True))
    )
    active_rules = list(result.scalars().all())

    active_job_ids: set[str] = set()

    for rule in active_rules:
        job_id = f"monitor_rule_{rule.id}"
        active_job_ids.add(job_id)

        schedule_kwargs = _SCHEDULE_MAP.get(rule.schedule, _SCHEDULE_MAP["daily"]).copy()
        trigger = schedule_kwargs.pop("trigger")

        existing_job = scheduler.get_job(job_id)
        if existing_job:
            # Reschedule in case the interval changed
            existing_job.reschedule(trigger=trigger, **schedule_kwargs)
            logger.debug("Rescheduled job %s", job_id)
        else:
            scheduler.add_job(
                _run_monitoring_check,
                trigger=trigger,
                id=job_id,
                args=[str(rule.org_id), str(rule.id)],
                replace_existing=True,
                **schedule_kwargs,
            )
            logger.info("Added monitoring job %s (schedule=%s)", job_id, rule.schedule)

    # Remove jobs for rules that are no longer active
    for job in scheduler.get_jobs():
        if job.id.startswith("monitor_rule_") and job.id not in active_job_ids:
            scheduler.remove_job(job.id)
            logger.info("Removed stale monitoring job %s", job.id)


async def _run_monitoring_check(org_id: str, rule_id: str) -> None:
    """Callback executed by APScheduler: opens a DB session and runs checks."""
    from app.core.database import async_session
    from app.services import monitoring_service

    try:
        async with async_session() as db:
            alerts = await monitoring_service.run_checks(
                db, UUID(org_id), UUID(rule_id)
            )
            if alerts:
                logger.info(
                    "Monitoring rule %s generated %d alert(s)", rule_id, len(alerts)
                )
                # Auto-create incident from monitoring failure
                from app.services import alert_engine
                from app.models.monitoring import MonitorRule
                rule_obj = (await db.execute(
                    select(MonitorRule).where(MonitorRule.id == UUID(rule_id))
                )).scalar_one_or_none()
                if rule_obj:
                    await alert_engine.create_auto_incident_from_monitor(
                        db, UUID(org_id), rule_obj.name or rule_obj.check_type,
                        rule_id, len(alerts),
                    )
            else:
                logger.debug("Monitoring rule %s passed.", rule_id)
    except Exception as exc:
        logger.error("Error running monitoring check for rule %s: %s", rule_id, exc)


async def _run_scheduled_collections() -> None:
    """Periodic job: run all due scheduled evidence collections."""
    from app.core.database import async_session
    from app.services import scheduled_collection_service

    try:
        async with async_session() as db:
            triggered = await scheduled_collection_service.run_scheduled_collections(db)
            if triggered:
                logger.info("Scheduled collections: triggered %d jobs.", triggered)
            else:
                logger.debug("Scheduled collections: no integrations due.")
    except Exception as exc:
        logger.error("Error running scheduled collections: %s", exc)


async def _run_control_tests() -> None:
    """Daily job: execute all active control test definitions."""
    from app.core.database import async_session
    from app.services import control_test_service

    try:
        async with async_session() as db:
            executed = await control_test_service.run_all_due_tests(db)
            if executed:
                logger.info("Control tests: executed %d tests.", executed)
            else:
                logger.debug("Control tests: no active definitions found.")
    except Exception as exc:
        logger.error("Error running control tests: %s", exc)


async def _run_alert_engine() -> None:
    """Periodic job: check evidence freshness + compliance regression."""
    from app.core.database import async_session
    from app.services import alert_engine

    try:
        async with async_session() as db:
            freshness_alerts = await alert_engine.check_evidence_freshness(db)
            regression_alerts = await alert_engine.check_compliance_regression(db)
            if freshness_alerts or regression_alerts:
                logger.info(
                    "Alert engine: %d freshness alerts, %d regression alerts",
                    freshness_alerts, regression_alerts,
                )
    except Exception as exc:
        logger.error("Error running alert engine: %s", exc)


async def _run_database_backup() -> None:
    """Nightly job: create a database backup."""
    from app.services import backup_service

    try:
        result = await backup_service.create_backup()
        logger.info("Nightly backup completed: %s (%s)", result["filename"], result["size_human"])
    except Exception as exc:
        logger.error("Nightly backup failed: %s", exc)


async def _run_retention_enforcement() -> None:
    """Nightly job: purge records that exceed their retention policy."""
    from app.core.database import async_session
    from app.services import privacy_service

    try:
        async with async_session() as db:
            purged = await privacy_service.enforce_retention(db)
            if purged:
                logger.info("Data retention: purged %d expired records.", purged)
            else:
                logger.debug("Data retention: no records to purge.")
    except Exception as exc:
        logger.error("Error enforcing data retention: %s", exc)


async def _run_scheduled_reports() -> None:
    """Hourly job: check for due report schedules, generate, and deliver via email."""
    from datetime import datetime, timezone, timedelta

    from app.core.database import async_session
    from app.models.report_schedule import ReportSchedule

    try:
        async with async_session() as db:
            result = await db.execute(
                select(ReportSchedule).where(ReportSchedule.is_active.is_(True))
            )
            schedules = list(result.scalars().all())

            now = datetime.now(timezone.utc)
            delivered = 0

            for schedule in schedules:
                if not _is_report_due(schedule, now):
                    continue

                try:
                    # Generate the report data
                    from app.services import report_service
                    from app.services.report_renderer import render_pdf
                    from app.services.notification_service import send_system_notification
                    from app.schemas.report import ReportCreate

                    # Create a report record
                    report_data_obj = ReportCreate(
                        title=f"Scheduled {schedule.report_type} report",
                        report_type=schedule.report_type,
                        format="pdf",
                    )
                    report = await report_service.create_report(
                        db, schedule.org_id, report_data_obj
                    )

                    # Generate and render
                    report_data = await report_service.generate_report_data(
                        db, schedule.org_id, report.id
                    )

                    # Notify via notification service
                    await send_system_notification(
                        db,
                        org_id=schedule.org_id,
                        category="report_delivery",
                        title=f"Scheduled Report: {schedule.report_type}",
                        message=(
                            f"Your scheduled {schedule.report_type} report has been generated "
                            f"and is ready for download."
                        ),
                        severity="info",
                        entity_type="report",
                        entity_id=str(report.id),
                    )

                    # Update last_sent_at
                    schedule.last_sent_at = now
                    await db.commit()
                    delivered += 1

                except Exception as inner_exc:
                    logger.error(
                        "Failed to deliver scheduled report %s: %s",
                        schedule.id,
                        inner_exc,
                    )

            if delivered:
                logger.info("Scheduled reports: delivered %d reports.", delivered)
            else:
                logger.debug("Scheduled reports: no reports due.")
    except Exception as exc:
        logger.error("Error running scheduled reports: %s", exc)


async def _run_policy_review_check() -> None:
    """Daily job: check for policies with overdue annual reviews and notify."""
    from datetime import datetime, timezone, timedelta

    from app.core.database import async_session
    from app.models.policy import Policy
    from app.services.notification_service import send_system_notification
    from sqlalchemy import or_

    try:
        async with async_session() as db:
            now = datetime.now(timezone.utc)
            one_year_ago = now - timedelta(days=365)

            # Find policies where:
            # 1. next_review_date is in the past, OR
            # 2. next_review_date is null AND published_at is older than 365 days
            result = await db.execute(
                select(Policy).where(
                    Policy.status.in_(["published", "approved"]),
                    or_(
                        Policy.next_review_date < now,
                        (Policy.next_review_date.is_(None)) & (Policy.published_at < one_year_ago),
                    ),
                )
            )
            overdue_policies = list(result.scalars().all())

            for policy in overdue_policies:
                await send_system_notification(
                    db,
                    org_id=policy.org_id,
                    category="policy_review",
                    title="Annual Review Due",
                    message=f"Annual review due for: {policy.title}",
                    severity="warning",
                    entity_type="policy",
                    entity_id=str(policy.id),
                )

            if overdue_policies:
                logger.info(
                    "Policy review check: %d overdue policies flagged.",
                    len(overdue_policies),
                )
            else:
                logger.debug("Policy review check: no overdue policies found.")
    except Exception as exc:
        logger.error("Error running policy review check: %s", exc)


def _is_report_due(schedule, now) -> bool:
    """Determine whether a report schedule is due for execution."""
    from datetime import timedelta

    last_sent = schedule.last_sent_at
    frequency = schedule.frequency

    # Never sent before — it's due
    if last_sent is None:
        return True

    if frequency == "daily":
        return (now - last_sent) >= timedelta(hours=23)
    elif frequency == "weekly":
        # Check if at least 6.5 days have passed and today is the right day of week
        if (now - last_sent) >= timedelta(days=6, hours=12):
            return now.weekday() == (schedule.day_of_week or 0)
        return False
    elif frequency == "monthly":
        # Check if at least 27 days have passed
        return (now - last_sent) >= timedelta(days=27)
    else:
        # Unknown frequency — default to weekly logic
        return (now - last_sent) >= timedelta(days=6, hours=12)
