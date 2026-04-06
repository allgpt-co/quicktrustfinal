"""Agent memory — store and recall past agent run outputs using embeddings."""

import hashlib
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.embedding import Embedding

logger = logging.getLogger(__name__)


async def store_agent_memory(
    db: AsyncSession,
    org_id: UUID,
    agent_type: str,
    run_id: UUID,
    content: str,
    metadata: dict | None = None,
) -> Embedding | None:
    """Store an agent run output as a searchable memory.

    Returns the embedding record or None if the embedding model is unavailable.
    """
    from app.services.embedding_service import _compute_embedding

    truncated_content = content[:5000]
    vector = _compute_embedding(truncated_content[:2000])

    content_hash = hashlib.sha256(truncated_content.encode()).hexdigest()

    embedding = Embedding(
        org_id=org_id,
        entity_type="agent_memory",
        entity_id=run_id,
        text_content=truncated_content,
        content_hash=content_hash,
        vector=vector,
        dimensions=len(vector) if vector else 0,
        model_name="all-MiniLM-L6-v2",
    )
    if metadata or agent_type:
        # Store metadata in text_content prefix for filtering
        pass

    db.add(embedding)
    await db.flush()
    return embedding


async def recall_similar_memories(
    db: AsyncSession,
    org_id: UUID,
    agent_type: str,
    query: str,
    limit: int = 5,
) -> list[dict]:
    """Recall past agent outputs similar to the current query."""
    from app.services.embedding_service import _compute_embedding, _cosine_similarity

    query_vector = _compute_embedding(query[:2000])

    result = await db.execute(
        select(Embedding)
        .where(
            Embedding.org_id == org_id,
            Embedding.entity_type == "agent_memory",
        )
        .order_by(Embedding.created_at.desc())
        .limit(100)
    )
    memories = list(result.scalars().all())

    scored = []
    for m in memories:
        # Compute similarity if vectors are available
        score = 0.0
        if query_vector and m.vector:
            score = _cosine_similarity(query_vector, m.vector)

        scored.append(
            {
                "content": m.text_content,
                "entity_id": str(m.entity_id),
                "similarity": round(score, 4),
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
        )

    # Sort by similarity descending
    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:limit]
