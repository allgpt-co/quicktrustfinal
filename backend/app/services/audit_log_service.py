"""Comprehensive audit logging service for security and compliance.

Records all entity changes, authentication events, admin actions, and
system events. Writes to both the database (for querying) and structured
stdout (for log aggregation by CloudWatch/ELK/Datadog).

Usage:
    from app.services.audit_log_service import (
        log_action, log_auth_event, log_data_event, log_admin_event
    )
"""

import json
import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core: write audit log entry
# ---------------------------------------------------------------------------

async def log_action(
    db: AsyncSession,
    org_id: UUID,
    actor_id: str,
    actor_type: str,
    action: str,
    entity_type: str,
    entity_id: str,
    *,
    event_type: str = "GENERAL",
    event_category: str = "system",
    severity: str = "INFO",
    outcome: str = "success",
    actor_email: str | None = None,
    actor_role: str | None = None,
    actor_ip: str | None = None,
    actor_user_agent: str | None = None,
    changes: dict | None = None,
    ip_address: str | None = None,
    request_id: str | None = None,
    session_id: str | None = None,
) -> AuditLog:
    """Create an audit log entry. Called after every mutation."""

    # Write structured log to stdout for log aggregation
    log_line = {
        "@timestamp": datetime.now(timezone.utc).isoformat(),
        "level": severity,
        "event_type": event_type,
        "event_category": event_category,
        "actor_id": actor_id,
        "actor_email": actor_email,
        "org_id": str(org_id),
        "resource": entity_type,
        "resource_id": entity_id,
        "action": action,
        "outcome": outcome,
        "request_id": request_id,
        "message": f"{event_type}: {action} on {entity_type} by {actor_email or actor_id}",
    }
    logger.info("[AUDIT] %s", json.dumps(log_line))

    entry = AuditLog(
        org_id=org_id,
        event_type=event_type,
        event_category=event_category,
        severity=severity,
        actor_type=actor_type,
        actor_id=str(actor_id),
        actor_email=actor_email,
        actor_role=actor_role,
        actor_ip=actor_ip or ip_address,
        actor_user_agent=actor_user_agent,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        outcome=outcome,
        changes=changes,
        ip_address=actor_ip or ip_address,
        request_id=request_id,
        session_id=session_id,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(entry)
    return entry


# ---------------------------------------------------------------------------
# Convenience: authentication events
# ---------------------------------------------------------------------------

async def log_auth_event(
    db: AsyncSession,
    org_id: UUID,
    event_type: str,
    actor_email: str,
    outcome: str,
    ip: str | None = None,
    user_agent: str | None = None,
    details: dict | None = None,
) -> AuditLog:
    """Log authentication events (login, logout, failed, locked, MFA)."""
    return await log_action(
        db=db,
        org_id=org_id,
        actor_id=actor_email,
        actor_type="user",
        action=event_type.lower(),
        entity_type="session",
        entity_id=actor_email,
        event_type=event_type,
        event_category="authentication",
        severity="WARN" if outcome == "failure" else "INFO",
        outcome=outcome,
        actor_email=actor_email,
        actor_ip=ip,
        actor_user_agent=user_agent,
        changes=details,
    )


# ---------------------------------------------------------------------------
# Convenience: data events (CRUD on entities)
# ---------------------------------------------------------------------------

async def log_data_event(
    db: AsyncSession,
    org_id: UUID,
    action: str,
    resource: str,
    resource_id: str,
    actor_id: str,
    actor_email: str,
    actor_role: str | None = None,
    ip: str | None = None,
    before: dict | None = None,
    after: dict | None = None,
    details: dict | None = None,
) -> AuditLog:
    """Log data mutation events (create, read, update, delete, export)."""
    changes = details or {}
    if before or after:
        changes["before"] = before
        changes["after"] = after

    return await log_action(
        db=db,
        org_id=org_id,
        actor_id=actor_id,
        actor_type="user",
        action=action,
        entity_type=resource,
        entity_id=str(resource_id),
        event_type=f"DATA_{action.upper()}",
        event_category="data",
        severity="WARN" if action == "delete" else "INFO",
        outcome="success",
        actor_email=actor_email,
        actor_role=actor_role,
        actor_ip=ip,
        changes=changes if changes else None,
    )


# ---------------------------------------------------------------------------
# Convenience: admin events
# ---------------------------------------------------------------------------

async def log_admin_event(
    db: AsyncSession,
    org_id: UUID,
    action: str,
    actor_id: str,
    actor_email: str,
    actor_role: str | None = None,
    ip: str | None = None,
    details: dict | None = None,
) -> AuditLog:
    """Log admin actions (user management, settings changes, etc.)."""
    return await log_action(
        db=db,
        org_id=org_id,
        actor_id=actor_id,
        actor_type="admin",
        action=action,
        entity_type="admin",
        entity_id="system",
        event_type="ADMIN_ACTION",
        event_category="admin",
        severity="WARN",
        outcome="success",
        actor_email=actor_email,
        actor_role=actor_role,
        actor_ip=ip,
        changes=details,
    )


# ---------------------------------------------------------------------------
# Convenience: AI/agent events
# ---------------------------------------------------------------------------

async def log_ai_event(
    db: AsyncSession,
    org_id: UUID,
    action: str,
    agent_name: str,
    actor_id: str,
    actor_email: str,
    details: dict | None = None,
) -> AuditLog:
    """Log AI agent events (runs, completions, approvals, rejections)."""
    return await log_action(
        db=db,
        org_id=org_id,
        actor_id=actor_id,
        actor_type="user",
        action=action,
        entity_type="agent",
        entity_id=agent_name,
        event_type="AI_AGENT_RUN",
        event_category="ai",
        severity="INFO",
        outcome="success",
        actor_email=actor_email,
        changes=details,
    )


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

async def list_audit_logs(
    db: AsyncSession,
    org_id: UUID,
    entity_type: str | None = None,
    entity_id: str | None = None,
    actor_id: str | None = None,
    action: str | None = None,
    event_type: str | None = None,
    event_category: str | None = None,
    severity: str | None = None,
    outcome: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[AuditLog], int]:
    base_q = select(AuditLog).where(AuditLog.org_id == org_id)
    count_q = select(func.count()).select_from(AuditLog).where(AuditLog.org_id == org_id)

    for attr, val in [
        (AuditLog.entity_type, entity_type),
        (AuditLog.entity_id, entity_id),
        (AuditLog.actor_id, actor_id),
        (AuditLog.action, action),
        (AuditLog.event_type, event_type),
        (AuditLog.event_category, event_category),
        (AuditLog.severity, severity),
        (AuditLog.outcome, outcome),
    ]:
        if val:
            base_q = base_q.where(attr == val)
            count_q = count_q.where(attr == val)

    if start_date:
        base_q = base_q.where(AuditLog.timestamp >= start_date)
        count_q = count_q.where(AuditLog.timestamp >= start_date)
    if end_date:
        base_q = base_q.where(AuditLog.timestamp <= end_date)
        count_q = count_q.where(AuditLog.timestamp <= end_date)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        AuditLog.timestamp.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_audit_log_stats(db: AsyncSession, org_id: UUID) -> dict:
    """Get summary statistics for audit logs."""
    total_q = select(func.count()).select_from(AuditLog).where(AuditLog.org_id == org_id)
    total = (await db.execute(total_q)).scalar() or 0

    # Get counts by category
    cat_q = (
        select(AuditLog.event_category, func.count())
        .where(AuditLog.org_id == org_id)
        .group_by(AuditLog.event_category)
    )
    cat_result = await db.execute(cat_q)
    by_category = {row[0]: row[1] for row in cat_result.all()}

    # Get counts by severity
    sev_q = (
        select(AuditLog.severity, func.count())
        .where(AuditLog.org_id == org_id)
        .group_by(AuditLog.severity)
    )
    sev_result = await db.execute(sev_q)
    by_severity = {row[0]: row[1] for row in sev_result.all()}

    # Get counts by action
    act_q = (
        select(AuditLog.action, func.count())
        .where(AuditLog.org_id == org_id)
        .group_by(AuditLog.action)
    )
    act_result = await db.execute(act_q)
    by_action = {row[0]: row[1] for row in act_result.all()}

    return {
        "total": total,
        "by_category": by_category,
        "by_severity": by_severity,
        "by_action": by_action,
    }
