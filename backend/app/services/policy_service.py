from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache_get, cache_set, cache_delete
from app.core.exceptions import BadRequestError, NotFoundError
from app.models.policy import Policy
from app.models.policy_template import PolicyTemplate
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyStatsResponse


async def list_policies(
    db: AsyncSession,
    org_id: UUID,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[Policy], int]:
    base_q = select(Policy).where(Policy.org_id == org_id)
    count_base = select(func.count()).select_from(Policy).where(Policy.org_id == org_id)

    if status:
        base_q = base_q.where(Policy.status == status)
        count_base = count_base.where(Policy.status == status)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(Policy.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_policy(db: AsyncSession, org_id: UUID, data: PolicyCreate) -> Policy:
    policy = Policy(org_id=org_id, **data.model_dump())
    db.add(policy)
    await db.commit()
    await db.refresh(policy)
    await cache_delete(f"org:{org_id}:policy_stats")
    return policy


async def get_policy(db: AsyncSession, org_id: UUID, policy_id: UUID) -> Policy:
    result = await db.execute(
        select(Policy).where(Policy.id == policy_id, Policy.org_id == org_id)
    )
    policy = result.scalar_one_or_none()
    if not policy:
        raise NotFoundError(f"Policy {policy_id} not found")
    return policy


async def update_policy(
    db: AsyncSession, org_id: UUID, policy_id: UUID, data: PolicyUpdate
) -> Policy:
    policy = await get_policy(db, org_id, policy_id)
    old_status = policy.status
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)

    # Track published_at timestamp
    new_status = update_data.get("status")
    if new_status == "published" and old_status != "published":
        policy.published_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(policy)

    # Policy distribution — notify when published
    if new_status == "published" and old_status != "published":
        try:
            await _distribute_policy(db, org_id, policy)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning("Policy distribution failed: %s", exc)

    # Create policy version snapshot on content/status changes
    if "content" in update_data or "status" in update_data:
        try:
            await _create_policy_version(db, org_id, policy)
        except Exception as exc:
            import logging
            logging.getLogger(__name__).warning("Failed to create policy version: %s", exc)

    return policy


async def _distribute_policy(db: AsyncSession, org_id: UUID, policy: Policy) -> None:
    """Notify all org users when a policy is published."""
    from app.models.user import User
    from app.services import alert_engine

    # Get all active users in the org
    result = await db.execute(
        select(User).where(User.org_id == org_id, User.is_active.is_(True))
    )
    users = list(result.scalars().all())

    # Create in-app notification for each user
    for user in users:
        await alert_engine.send_notification(
            db, org_id,
            title=f"New Policy Published: {policy.title}",
            message=f"The policy '{policy.title}' (v{policy.version}) has been published. Please review and acknowledge.",
            severity="info",
            category="policy_published",
            user_id=user.id,
            entity_type="policy",
            entity_id=str(policy.id),
        )

    # Also send a Slack notification if configured
    await alert_engine.send_slack_if_configured(
        db, org_id,
        title=f"📋 Policy Published: {policy.title}",
        message=f"Version {policy.version} is now live. {len(users)} team members notified.",
        severity="info",
    )


async def _create_policy_version(db: AsyncSession, org_id: UUID, policy: Policy) -> None:
    """Create a version snapshot of the current policy state."""
    from app.models.policy_version import PolicyVersion

    # Get the latest version number
    result = await db.execute(
        select(func.max(PolicyVersion.version_number))
        .where(PolicyVersion.policy_id == policy.id, PolicyVersion.org_id == org_id)
    )
    max_ver = result.scalar() or 0

    version = PolicyVersion(
        policy_id=policy.id,
        org_id=org_id,
        version_number=max_ver + 1,
        content=policy.content or "",
        status_at_version=policy.status,
        change_summary=f"Status changed to {policy.status}",
    )
    db.add(version)
    await db.commit()


async def delete_policy(db: AsyncSession, org_id: UUID, policy_id: UUID) -> None:
    policy = await get_policy(db, org_id, policy_id)
    await db.delete(policy)
    await db.commit()
    await cache_delete(f"org:{org_id}:policy_stats")


async def get_policy_stats(db: AsyncSession, org_id: UUID) -> PolicyStatsResponse:
    cache_key = f"org:{org_id}:policy_stats"
    cached = await cache_get(cache_key)
    if cached:
        return PolicyStatsResponse(**cached)

    result = await db.execute(
        select(
            func.count().label("total"),
            func.count().filter(Policy.status == "draft").label("draft"),
            func.count().filter(Policy.status == "in_review").label("in_review"),
            func.count().filter(Policy.status == "approved").label("approved"),
            func.count().filter(Policy.status == "published").label("published"),
            func.count().filter(Policy.status == "archived").label("archived"),
        )
        .select_from(Policy)
        .where(Policy.org_id == org_id)
    )
    row = result.one()
    stats = PolicyStatsResponse(
        total=row.total,
        draft=row.draft,
        in_review=row.in_review,
        approved=row.approved,
        published=row.published,
        archived=row.archived,
    )
    await cache_set(cache_key, stats.model_dump(), ttl=120)
    return stats


async def list_policy_templates(
    db: AsyncSession,
    category: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[PolicyTemplate], int]:
    base_q = select(PolicyTemplate)
    count_base = select(func.count()).select_from(PolicyTemplate)

    if category:
        base_q = base_q.where(PolicyTemplate.category == category)
        count_base = count_base.where(PolicyTemplate.category == category)

    total = (await db.execute(count_base)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(PolicyTemplate.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_policy_template(db: AsyncSession, template_id: UUID) -> PolicyTemplate:
    result = await db.execute(
        select(PolicyTemplate).where(PolicyTemplate.id == template_id)
    )
    template = result.scalar_one_or_none()
    if not template:
        raise NotFoundError(f"Policy template {template_id} not found")
    return template


# ---------------------------------------------------------------------------
# Policy workflow transitions
# ---------------------------------------------------------------------------

async def submit_for_review(
    db: AsyncSession, org_id: UUID, policy_id: UUID, user_id: UUID
) -> Policy:
    """Transition a policy from 'draft' to 'in_review'."""
    policy = await get_policy(db, org_id, policy_id)
    if policy.status != "draft":
        raise BadRequestError(
            f"Cannot submit for review: policy is '{policy.status}', expected 'draft'."
        )
    policy.status = "in_review"
    await db.commit()
    await db.refresh(policy)
    await cache_delete(f"org:{org_id}:policy_stats")
    return policy


async def approve_policy(
    db: AsyncSession, org_id: UUID, policy_id: UUID, user_id: UUID
) -> Policy:
    """Transition a policy from 'in_review' to 'approved'."""
    policy = await get_policy(db, org_id, policy_id)
    if policy.status != "in_review":
        raise BadRequestError(
            f"Cannot approve: policy is '{policy.status}', expected 'in_review'."
        )
    policy.status = "approved"
    policy.approved_by_id = user_id
    policy.approved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(policy)
    await cache_delete(f"org:{org_id}:policy_stats")
    return policy


async def publish_policy(
    db: AsyncSession, org_id: UUID, policy_id: UUID, user_id: UUID
) -> Policy:
    """Transition a policy from 'approved' to 'published'."""
    policy = await get_policy(db, org_id, policy_id)
    if policy.status != "approved":
        raise BadRequestError(
            f"Cannot publish: policy is '{policy.status}', expected 'approved'."
        )
    policy.status = "published"
    policy.published_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(policy)
    await cache_delete(f"org:{org_id}:policy_stats")
    return policy


async def archive_policy(
    db: AsyncSession, org_id: UUID, policy_id: UUID
) -> Policy:
    """Archive a policy (any current status)."""
    policy = await get_policy(db, org_id, policy_id)
    policy.status = "archived"
    await db.commit()
    await db.refresh(policy)
    await cache_delete(f"org:{org_id}:policy_stats")
    return policy
