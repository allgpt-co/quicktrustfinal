"""Service for incident playbook management."""
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.playbook import IncidentPlaybook, PlaybookExecution
from app.schemas.playbook import PlaybookCreate, PlaybookUpdate


# ---------------------------------------------------------------------------
# Default playbooks seeded on first use
# ---------------------------------------------------------------------------

DEFAULT_PLAYBOOKS = [
    {
        "title": "Data Breach Response",
        "description": "Step-by-step response plan for confirmed or suspected data breaches. Covers containment, investigation, notification, and recovery.",
        "severity_trigger": "P1",
        "category_trigger": "data_breach",
        "steps": [
            {"order": 1, "title": "Contain the Breach", "description": "Isolate affected systems, revoke compromised credentials, block malicious IPs.", "assignee_role": "security_team", "sla_hours": 1},
            {"order": 2, "title": "Assess Scope & Impact", "description": "Determine what data was exposed, how many records affected, and attack vector.", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 3, "title": "Preserve Evidence", "description": "Capture forensic images, export logs, document timeline of events.", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 4, "title": "Notify Legal & Compliance", "description": "Inform legal counsel and compliance team. Begin GDPR 72h / HIPAA notification clock.", "assignee_role": "compliance_manager", "sla_hours": 8},
            {"order": 5, "title": "Notify Affected Parties", "description": "Prepare and send breach notification to affected users/customers per regulatory requirements.", "assignee_role": "compliance_manager", "sla_hours": 72},
            {"order": 6, "title": "Remediate Root Cause", "description": "Patch vulnerability, update configurations, rotate all potentially compromised secrets.", "assignee_role": "engineering", "sla_hours": 48},
            {"order": 7, "title": "Post-Incident Review", "description": "Conduct post-mortem, document lessons learned, update playbook if needed.", "assignee_role": "security_team", "sla_hours": 168},
        ],
        "notification_channels": ["slack:#security-incidents", "email:security@company.com"],
        "compliance_references": ["SOC 2 CC7.3", "SOC 2 CC7.4", "GDPR Art. 33", "GDPR Art. 34", "HIPAA §164.408"],
    },
    {
        "title": "DDoS Attack Response",
        "description": "Response plan for distributed denial-of-service attacks targeting company infrastructure.",
        "severity_trigger": "P1",
        "category_trigger": "ddos",
        "steps": [
            {"order": 1, "title": "Detect & Classify Attack", "description": "Confirm DDoS, classify type (volumetric, protocol, application layer), identify targets.", "assignee_role": "security_team", "sla_hours": 0.5},
            {"order": 2, "title": "Activate DDoS Mitigation", "description": "Enable CDN/WAF rate limiting, activate DDoS protection service, implement geo-blocking if needed.", "assignee_role": "infrastructure", "sla_hours": 1},
            {"order": 3, "title": "Scale Infrastructure", "description": "Increase capacity, enable auto-scaling, distribute traffic across regions.", "assignee_role": "infrastructure", "sla_hours": 2},
            {"order": 4, "title": "Communicate Status", "description": "Update status page, notify customers, inform leadership on impact.", "assignee_role": "compliance_manager", "sla_hours": 2},
            {"order": 5, "title": "Monitor & Adjust", "description": "Continuously monitor attack patterns, adjust mitigation rules, track service availability.", "assignee_role": "security_team", "sla_hours": 24},
            {"order": 6, "title": "Post-Attack Analysis", "description": "Analyze attack patterns, update firewall rules, improve detection thresholds.", "assignee_role": "security_team", "sla_hours": 72},
        ],
        "notification_channels": ["slack:#infrastructure", "slack:#security-incidents"],
        "compliance_references": ["SOC 2 CC7.2", "SOC 2 CC7.3"],
    },
    {
        "title": "Unauthorized Access Response",
        "description": "Response plan for detected unauthorized access to systems, accounts, or data.",
        "severity_trigger": "P2",
        "category_trigger": "unauthorized_access",
        "steps": [
            {"order": 1, "title": "Disable Compromised Account", "description": "Immediately disable the compromised account, revoke all sessions and API keys.", "assignee_role": "security_team", "sla_hours": 0.5},
            {"order": 2, "title": "Assess Extent of Access", "description": "Review audit logs to determine what was accessed, modified, or exfiltrated.", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 3, "title": "Reset Credentials", "description": "Force password reset for affected user, rotate any shared credentials or secrets.", "assignee_role": "security_team", "sla_hours": 2},
            {"order": 4, "title": "Investigate Root Cause", "description": "Determine how access was obtained — phishing, credential stuffing, insider, stolen device.", "assignee_role": "security_team", "sla_hours": 24},
            {"order": 5, "title": "Implement Controls", "description": "Add MFA if missing, update access policies, enhance monitoring on affected systems.", "assignee_role": "engineering", "sla_hours": 48},
            {"order": 6, "title": "Document & Close", "description": "Complete incident report, update risk register, notify affected parties if data was accessed.", "assignee_role": "compliance_manager", "sla_hours": 72},
        ],
        "notification_channels": ["slack:#security-incidents"],
        "compliance_references": ["SOC 2 CC6.1", "SOC 2 CC6.8", "SOC 2 CC7.3"],
    },
    {
        "title": "Malware Infection Response",
        "description": "Response plan for detected malware on company devices or servers.",
        "severity_trigger": "P2",
        "category_trigger": "malware",
        "steps": [
            {"order": 1, "title": "Isolate Infected System", "description": "Disconnect system from network, disable network interfaces, quarantine the device.", "assignee_role": "security_team", "sla_hours": 0.5},
            {"order": 2, "title": "Identify Malware Type", "description": "Run AV scan, identify malware family, check IOCs (indicators of compromise).", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 3, "title": "Check for Lateral Movement", "description": "Scan other systems for same IOCs, review network logs for suspicious connections.", "assignee_role": "security_team", "sla_hours": 8},
            {"order": 4, "title": "Clean & Restore", "description": "Remove malware, restore from clean backup if needed, verify system integrity.", "assignee_role": "infrastructure", "sla_hours": 24},
            {"order": 5, "title": "Update Defenses", "description": "Add IOCs to blocklists, update AV signatures, patch exploited vulnerability.", "assignee_role": "security_team", "sla_hours": 48},
            {"order": 6, "title": "User Awareness", "description": "Notify affected user, conduct targeted training if infection was via phishing.", "assignee_role": "compliance_manager", "sla_hours": 72},
        ],
        "notification_channels": ["slack:#security-incidents"],
        "compliance_references": ["SOC 2 CC6.8", "SOC 2 CC7.2", "ISO 27001 A.12.2"],
    },
    {
        "title": "Insider Threat Response",
        "description": "Response plan for suspected or confirmed insider threat activity (data theft, sabotage, policy violations by employees).",
        "severity_trigger": "P2",
        "category_trigger": "insider_threat",
        "steps": [
            {"order": 1, "title": "Verify & Document Suspicion", "description": "Review alerting data, audit logs, and DLP reports. Document evidence without alerting the subject.", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 2, "title": "Involve HR & Legal", "description": "Brief HR and legal counsel before taking action. Determine investigation scope.", "assignee_role": "compliance_manager", "sla_hours": 8},
            {"order": 3, "title": "Increase Monitoring", "description": "Enable enhanced logging on subject's accounts, monitor file access and email activity.", "assignee_role": "security_team", "sla_hours": 4},
            {"order": 4, "title": "Preserve Evidence", "description": "Create forensic copies of relevant data, export email and chat logs, screenshot suspicious activity.", "assignee_role": "security_team", "sla_hours": 24},
            {"order": 5, "title": "Contain & Remediate", "description": "If confirmed: disable access, collect devices, revoke credentials. HR handles employment actions.", "assignee_role": "security_team", "sla_hours": 48},
            {"order": 6, "title": "Review & Improve Controls", "description": "Assess what controls failed, implement DLP rules, update access review frequency.", "assignee_role": "compliance_manager", "sla_hours": 168},
        ],
        "notification_channels": ["email:security@company.com"],
        "compliance_references": ["SOC 2 CC6.1", "SOC 2 CC7.2", "SOC 2 CC7.4"],
    },
]


async def seed_default_playbooks(db: AsyncSession, org_id: UUID) -> int:
    """Seed default playbooks for an organization. Returns count created."""
    existing = await db.execute(
        select(func.count()).select_from(IncidentPlaybook).where(
            IncidentPlaybook.org_id == org_id, IncidentPlaybook.is_default.is_(True)
        )
    )
    if (existing.scalar() or 0) > 0:
        return 0

    count = 0
    for pb_data in DEFAULT_PLAYBOOKS:
        pb = IncidentPlaybook(
            org_id=org_id,
            title=pb_data["title"],
            description=pb_data["description"],
            severity_trigger=pb_data.get("severity_trigger"),
            category_trigger=pb_data.get("category_trigger"),
            is_default=True,
            is_active=True,
            steps=[s if isinstance(s, dict) else s.model_dump() for s in pb_data["steps"]],
            notification_channels=pb_data.get("notification_channels", []),
            compliance_references=pb_data.get("compliance_references", []),
        )
        db.add(pb)
        count += 1
    await db.commit()
    return count


async def list_playbooks(
    db: AsyncSession, org_id: UUID, page: int = 1, page_size: int = 50
) -> tuple[list[IncidentPlaybook], int]:
    count_q = select(func.count()).select_from(IncidentPlaybook).where(
        IncidentPlaybook.org_id == org_id
    )
    total = (await db.execute(count_q)).scalar() or 0
    q = (
        select(IncidentPlaybook)
        .where(IncidentPlaybook.org_id == org_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(IncidentPlaybook.created_at.desc())
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_playbook(
    db: AsyncSession, org_id: UUID, playbook_id: UUID
) -> IncidentPlaybook:
    result = await db.execute(
        select(IncidentPlaybook).where(
            IncidentPlaybook.id == playbook_id, IncidentPlaybook.org_id == org_id
        )
    )
    pb = result.scalar_one_or_none()
    if not pb:
        raise NotFoundError(f"Playbook {playbook_id} not found")
    return pb


async def create_playbook(
    db: AsyncSession, org_id: UUID, data: PlaybookCreate
) -> IncidentPlaybook:
    pb = IncidentPlaybook(
        org_id=org_id,
        title=data.title,
        description=data.description,
        severity_trigger=data.severity_trigger,
        category_trigger=data.category_trigger,
        steps=[s.model_dump() for s in data.steps],
        notification_channels=data.notification_channels,
        compliance_references=data.compliance_references,
    )
    db.add(pb)
    await db.commit()
    await db.refresh(pb)
    return pb


async def update_playbook(
    db: AsyncSession, org_id: UUID, playbook_id: UUID, data: PlaybookUpdate
) -> IncidentPlaybook:
    pb = await get_playbook(db, org_id, playbook_id)
    update_data = data.model_dump(exclude_unset=True)
    if "steps" in update_data and update_data["steps"] is not None:
        update_data["steps"] = [
            s.model_dump() if hasattr(s, "model_dump") else s
            for s in update_data["steps"]
        ]
    for field, value in update_data.items():
        setattr(pb, field, value)
    await db.commit()
    await db.refresh(pb)
    return pb


async def delete_playbook(
    db: AsyncSession, org_id: UUID, playbook_id: UUID
) -> None:
    pb = await get_playbook(db, org_id, playbook_id)
    await db.delete(pb)
    await db.commit()


async def trigger_playbook(
    db: AsyncSession, org_id: UUID, playbook_id: UUID, incident_id: UUID
) -> PlaybookExecution:
    """Start executing a playbook for an incident."""
    pb = await get_playbook(db, org_id, playbook_id)
    steps = pb.steps or []
    step_statuses = [
        {"step_index": i, "status": "pending", "completed_by": None, "completed_at": None, "notes": None}
        for i in range(len(steps))
    ]
    execution = PlaybookExecution(
        org_id=org_id,
        playbook_id=playbook_id,
        incident_id=incident_id,
        status="in_progress",
        current_step=0,
        step_statuses=step_statuses,
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    return execution


async def complete_step(
    db: AsyncSession, org_id: UUID, execution_id: UUID,
    completed_by_id: UUID | None = None, notes: str | None = None,
) -> PlaybookExecution:
    """Complete the current step and advance to the next."""
    result = await db.execute(
        select(PlaybookExecution).where(
            PlaybookExecution.id == execution_id, PlaybookExecution.org_id == org_id
        )
    )
    execution = result.scalar_one_or_none()
    if not execution:
        raise NotFoundError(f"Playbook execution {execution_id} not found")

    step_statuses = list(execution.step_statuses or [])
    idx = execution.current_step
    if idx < len(step_statuses):
        step_statuses[idx] = {
            **step_statuses[idx],
            "status": "completed",
            "completed_by": str(completed_by_id) if completed_by_id else None,
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "notes": notes,
        }

    next_step = idx + 1
    if next_step >= len(step_statuses):
        execution.status = "completed"
    execution.current_step = next_step
    execution.step_statuses = step_statuses
    await db.commit()
    await db.refresh(execution)
    return execution


async def auto_trigger_playbook(
    db: AsyncSession, org_id: UUID, incident_id: UUID,
    severity: str, category: str | None,
) -> PlaybookExecution | None:
    """Auto-trigger a playbook based on incident severity/category."""
    q = select(IncidentPlaybook).where(
        IncidentPlaybook.org_id == org_id,
        IncidentPlaybook.is_active.is_(True),
    )
    if category:
        # Prefer category match
        result = await db.execute(
            q.where(IncidentPlaybook.category_trigger == category)
        )
        pb = result.scalar_one_or_none()
        if pb:
            return await trigger_playbook(db, org_id, pb.id, incident_id)

    # Fall back to severity match
    result = await db.execute(
        q.where(IncidentPlaybook.severity_trigger == severity)
    )
    pb = result.scalars().first()
    if pb:
        return await trigger_playbook(db, org_id, pb.id, incident_id)
    return None


async def list_executions(
    db: AsyncSession, org_id: UUID, incident_id: UUID | None = None,
) -> list[PlaybookExecution]:
    q = select(PlaybookExecution).where(PlaybookExecution.org_id == org_id)
    if incident_id:
        q = q.where(PlaybookExecution.incident_id == incident_id)
    q = q.order_by(PlaybookExecution.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all())
