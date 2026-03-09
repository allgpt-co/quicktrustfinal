from uuid import UUID
from datetime import datetime, timezone
import logging

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import select, func

from app.core.dependencies import DB, CurrentUser, AnyInternalUser, ComplianceUser, VerifiedOrgId
from app.core.exceptions import NotFoundError
from app.core.rate_limit import limiter
from app.core.task_runner import create_safe_task
from app.models.agent_run import AgentRun
from app.schemas.agent_run import AgentRunApproval, AgentRunResponse, AgentRunTrigger, AgentRunTriggerGeneric
from app.schemas.common import PaginatedResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/organizations/{org_id}/agents", tags=["agents"])


# ---------------------------------------------------------------------------
# Helper: run an agent in a background task using a dedicated DB session
# ---------------------------------------------------------------------------

async def _execute_agent(agent_run_id: str, org_id: str, agent_type: str, input_data: dict):
    """Generic background task that dispatches to the correct agent graph."""
    logger.info("_execute_agent STARTED: run=%s type=%s org=%s", agent_run_id, agent_type, org_id)

    try:
        from app.core.database import bg_async_session

        async with bg_async_session() as db:
            run = await db.get(AgentRun, agent_run_id)
            if not run:
                logger.error("Agent run %s not found", agent_run_id)
                return

            run.status = "running"
            run.started_at = datetime.now(timezone.utc)
            await db.commit()

            try:
                logger.info("Dispatching agent %s for run %s", agent_type, agent_run_id)
                result = await _dispatch_agent(
                    agent_type, db, org_id, agent_run_id, input_data,
                )
                run.status = "completed"
                run.approval_status = "pending_review"
                run.output_data = result
                run.completed_at = datetime.now(timezone.utc)
                logger.info("Agent %s completed for run %s", agent_type, agent_run_id)
            except Exception as e:
                logger.error("Agent %s failed: %s", agent_type, e, exc_info=True)
                run.status = "failed"
                run.error_message = str(e)[:2000]
                run.completed_at = datetime.now(timezone.utc)

            await db.commit()
    except Exception as e:
        logger.error("Background task for %s critically failed: %s", agent_run_id, e, exc_info=True)
        # Try to mark as failed with a fresh session
        try:
            from app.core.database import bg_async_session
            async with bg_async_session() as db:
                run = await db.get(AgentRun, agent_run_id)
                if run and run.status != "failed":
                    run.status = "failed"
                    run.error_message = f"Critical error: {str(e)[:1900]}"
                    run.completed_at = datetime.now(timezone.utc)
                    await db.commit()
        except Exception:
            pass


async def _dispatch_agent(agent_type: str, db, org_id: str, agent_run_id: str, input_data: dict):
    """Import and call the correct agent graph function."""
    fw_id = input_data.get("framework_id")
    ctx = input_data.get("company_context", {})

    if agent_type == "controls_generation":
        from app.agents.controls_generation.graph import run_controls_generation
        return await run_controls_generation(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            framework_id=fw_id, company_context=ctx,
        )
    elif agent_type == "policy_generation":
        from app.agents.policy_generation.graph import run_policy_generation
        return await run_policy_generation(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            framework_id=fw_id, company_context=ctx,
        )
    elif agent_type == "evidence_generation":
        from app.agents.evidence_generation.graph import run_evidence_generation
        return await run_evidence_generation(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            company_context=ctx,
        )
    elif agent_type == "risk_assessment":
        from app.agents.risk_assessment.graph import run_risk_assessment
        return await run_risk_assessment(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            framework_id=fw_id,
        )
    elif agent_type == "remediation":
        from app.agents.remediation.graph import run_remediation
        return await run_remediation(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
        )
    elif agent_type == "audit_preparation":
        from app.agents.audit_preparation.graph import run_audit_preparation
        return await run_audit_preparation(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            audit_id=input_data.get("audit_id"),
        )
    elif agent_type == "vendor_risk_assessment":
        from app.agents.vendor_risk_assessment.graph import run_vendor_risk_assessment
        return await run_vendor_risk_assessment(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
            vendor_id=input_data.get("vendor_id"),
        )
    elif agent_type == "pentest_orchestrator":
        from app.agents.pentest_orchestrator.graph import run_pentest_orchestrator
        return await run_pentest_orchestrator(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
        )
    elif agent_type == "monitoring_daemon":
        from app.agents.monitoring_daemon.graph import run_monitoring_daemon
        return await run_monitoring_daemon(
            db=db, org_id=org_id, agent_run_id=agent_run_id,
        )
    else:
        raise ValueError(f"Unknown agent type: {agent_type}")


# ---------------------------------------------------------------------------
# Trigger endpoints
# ---------------------------------------------------------------------------

@router.post("/controls-generation/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_controls_generation(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTrigger,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"framework_id": str(data.framework_id), "company_context": data.company_context or {}}
    agent_run = AgentRun(
        org_id=org_id, agent_type="controls_generation", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "controls_generation", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/policy-generation/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_policy_generation(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTrigger,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"framework_id": str(data.framework_id), "company_context": data.company_context or {}}
    agent_run = AgentRun(
        org_id=org_id, agent_type="policy_generation", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "policy_generation", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/evidence-generation/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_evidence_generation(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTrigger,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"framework_id": str(data.framework_id), "company_context": data.company_context or {}}
    agent_run = AgentRun(
        org_id=org_id, agent_type="evidence_generation", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "evidence_generation", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/risk-assessment/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_risk_assessment(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"framework_id": str(data.framework_id) if data.framework_id else None}
    agent_run = AgentRun(
        org_id=org_id, agent_type="risk_assessment", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "risk_assessment", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/remediation/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_remediation(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    agent_run = AgentRun(
        org_id=org_id, agent_type="remediation", trigger="manual",
        status="pending", input_data={},
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "remediation", {}),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/audit-preparation/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_audit_preparation(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"audit_id": str(data.audit_id) if data.audit_id else None}
    agent_run = AgentRun(
        org_id=org_id, agent_type="audit_preparation", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "audit_preparation", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/vendor-risk-assessment/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_vendor_risk_assessment(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    input_data = {"vendor_id": str(data.vendor_id) if data.vendor_id else None}
    agent_run = AgentRun(
        org_id=org_id, agent_type="vendor_risk_assessment", trigger="manual",
        status="pending", input_data=input_data,
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "vendor_risk_assessment", input_data),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/pentest-orchestrator/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_pentest_orchestrator(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    agent_run = AgentRun(
        org_id=org_id, agent_type="pentest_orchestrator", trigger="manual",
        status="pending", input_data={},
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "pentest_orchestrator", {}),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


@router.post("/monitoring-daemon/run", response_model=AgentRunResponse, status_code=201)
@limiter.limit("10/minute")
async def trigger_monitoring_daemon(
    request: Request, org_id: VerifiedOrgId, data: AgentRunTriggerGeneric,
    db: DB, current_user: ComplianceUser,
):
    agent_run = AgentRun(
        org_id=org_id, agent_type="monitoring_daemon", trigger="manual",
        status="pending", input_data={},
    )
    db.add(agent_run)
    await db.commit()
    create_safe_task(
        _execute_agent(str(agent_run.id), str(org_id), "monitoring_daemon", {}),
        agent_run_id=agent_run.id, org_id=org_id,
    )
    return agent_run


# ---------------------------------------------------------------------------
# Approval / Rejection
# ---------------------------------------------------------------------------

@router.post("/runs/{run_id}/approve", response_model=AgentRunResponse)
async def approve_agent_run(
    org_id: VerifiedOrgId, run_id: UUID, db: DB, current_user: ComplianceUser,
):
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id, AgentRun.org_id == org_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError(f"Agent run {run_id} not found")
    if run.approval_status != "pending_review":
        raise HTTPException(400, "Agent run is not pending review")

    run.approval_status = "approved"
    run.approved_by = current_user.id
    run.approved_at = datetime.now(timezone.utc)
    await db.commit()
    return run


@router.post("/runs/{run_id}/reject", response_model=AgentRunResponse)
async def reject_agent_run(
    org_id: VerifiedOrgId, run_id: UUID, body: AgentRunApproval,
    db: DB, current_user: ComplianceUser,
):
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id, AgentRun.org_id == org_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError(f"Agent run {run_id} not found")
    if run.approval_status != "pending_review":
        raise HTTPException(400, "Agent run is not pending review")

    run.approval_status = "rejected"
    reason = body.reason or "No reason provided"
    run.error_message = f"Rejected: {reason}"
    await db.commit()
    return run


# ---------------------------------------------------------------------------
# List / Get runs
# ---------------------------------------------------------------------------

@router.get("/runs", response_model=PaginatedResponse)
async def list_runs(
    org_id: VerifiedOrgId, db: DB, current_user: AnyInternalUser,
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
):
    count_q = select(func.count()).select_from(AgentRun).where(AgentRun.org_id == org_id)
    total = (await db.execute(count_q)).scalar() or 0

    q = (
        select(AgentRun)
        .where(AgentRun.org_id == org_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .order_by(AgentRun.created_at.desc())
    )
    result = await db.execute(q)
    items = [AgentRunResponse.model_validate(r) for r in result.scalars().all()]

    return PaginatedResponse(
        items=items, total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


@router.get("/runs/{run_id}", response_model=AgentRunResponse)
async def get_run(org_id: VerifiedOrgId, run_id: UUID, db: DB, current_user: AnyInternalUser):
    result = await db.execute(
        select(AgentRun).where(AgentRun.id == run_id, AgentRun.org_id == org_id)
    )
    run = result.scalar_one_or_none()
    if not run:
        raise NotFoundError(f"Agent run {run_id} not found")
    return run
