"""Agent memory API — recall past agent run outputs via semantic search."""

from uuid import UUID

from fastapi import APIRouter, Query

from app.core.dependencies import DB, AnyInternalUser, VerifiedOrgId
from app.services import agent_memory

router = APIRouter(
    prefix="/organizations/{org_id}/agent-memory",
    tags=["agent-memory"],
)


@router.get("")
async def recall_memories(
    org_id: VerifiedOrgId,
    db: DB,
    current_user: AnyInternalUser,
    agent_type: str = Query(..., description="Type of agent (e.g. risk_assessment)"),
    query: str = Query(..., description="Query text to find similar past runs"),
    limit: int = Query(5, ge=1, le=50),
):
    """Recall past agent outputs similar to the current query."""
    memories = await agent_memory.recall_similar_memories(
        db, org_id, agent_type, query, limit=limit,
    )
    return {"agent_type": agent_type, "results": memories, "total": len(memories)}
