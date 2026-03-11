"""Questionnaire auto-fill agent nodes.

Wraps the existing questionnaire_service.auto_fill logic into the
LangGraph agent pattern so runs are tracked alongside other agents.
"""
import uuid
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.questionnaire_agent.state import QuestionnaireAgentState
from app.models.questionnaire import Questionnaire
from app.models.control import Control
from app.models.policy import Policy

logger = logging.getLogger(__name__)


async def load_questionnaires(state: QuestionnaireAgentState, db: AsyncSession) -> dict:
    """Load target questionnaire(s) and org context (controls + policies)."""
    org_id = state["org_id"]
    questionnaire_id = state.get("questionnaire_id")

    # Load questionnaire(s)
    q = select(Questionnaire).where(Questionnaire.org_id == uuid.UUID(org_id))
    if questionnaire_id:
        q = q.where(Questionnaire.id == uuid.UUID(questionnaire_id))
    else:
        # Process all draft/in_progress questionnaires
        q = q.where(Questionnaire.status.in_(["draft", "in_progress"]))

    result = await db.execute(q)
    questionnaires = list(result.scalars().all())

    if not questionnaires:
        return {"error": "No questionnaires found to process"}

    # Load controls and policies for matching context
    controls_result = await db.execute(
        select(Control).where(Control.org_id == uuid.UUID(org_id))
    )
    controls = list(controls_result.scalars().all())

    policies_result = await db.execute(
        select(Policy).where(Policy.org_id == uuid.UUID(org_id))
    )
    policies = list(policies_result.scalars().all())

    controls_context = "\n".join(
        f"- {ctrl.title} (status: {ctrl.status})"
        + (f" — {ctrl.description[:200]}" if getattr(ctrl, "description", None) else "")
        for ctrl in controls
    ) or "(no controls defined)"

    policies_context = "\n".join(
        f"- {pol.title} (status: {pol.status})"
        + (f" — {pol.description[:200]}" if getattr(pol, "description", None) else "")
        for pol in policies
    ) or "(no policies defined)"

    return {
        "questionnaires": [
            {
                "id": str(q.id),
                "title": q.title,
                "total_questions": q.total_questions,
                "answered_count": q.answered_count,
                "questions": q.questions or [],
            }
            for q in questionnaires
        ],
        "controls_context": controls_context,
        "policies_context": policies_context,
    }


async def auto_fill_questionnaires(state: QuestionnaireAgentState, db: AsyncSession) -> dict:
    """Run auto-fill on each questionnaire using the existing service logic."""
    from app.services.questionnaire_service import auto_fill

    org_id = uuid.UUID(state["org_id"])
    questionnaires = state.get("questionnaires", [])
    results = []
    total_filled = 0

    for q_info in questionnaires:
        q_id = uuid.UUID(q_info["id"])
        try:
            filled = await auto_fill(db, org_id, q_id)
            total_filled += filled
            results.append({
                "questionnaire_id": q_info["id"],
                "title": q_info["title"],
                "questions_filled": filled,
                "status": "completed",
            })
            logger.info(
                "Auto-filled %d answers for questionnaire %s (%s)",
                filled, q_info["id"], q_info["title"],
            )
        except Exception as e:
            logger.error("Auto-fill failed for questionnaire %s: %s", q_info["id"], e)
            results.append({
                "questionnaire_id": q_info["id"],
                "title": q_info["title"],
                "questions_filled": 0,
                "status": "failed",
                "error": str(e)[:500],
            })

    return {
        "results_by_questionnaire": results,
        "total_filled": total_filled,
        "total_questionnaires": len(questionnaires),
    }


async def summarize_results(state: QuestionnaireAgentState, db: AsyncSession) -> dict:
    """Generate a final summary of auto-fill results."""
    results = state.get("results_by_questionnaire", [])
    total_filled = state.get("total_filled", 0)
    total_qs = state.get("total_questionnaires", 0)

    succeeded = sum(1 for r in results if r["status"] == "completed")
    failed = sum(1 for r in results if r["status"] == "failed")

    logger.info(
        "Questionnaire agent completed: %d questionnaires processed "
        "(%d succeeded, %d failed), %d total answers filled",
        total_qs, succeeded, failed, total_filled,
    )

    return {
        "results_by_questionnaire": results,
        "total_filled": total_filled,
        "total_questionnaires": total_qs,
    }
