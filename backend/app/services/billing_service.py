"""Plan configuration and tenant-scoped entitlement resolution; no provider calls."""
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.models.audit_log import AuditLog
from app.models.billing import Plan, Subscription
from app.models.organization import Organization
from app.schemas.billing import BillingResponse, EntitlementResponse, Limits, SubscriptionResponse


def _audit(db, actor, org_id, action, entity, entity_id, changes):
    # Same transaction as the write: a configuration change cannot lose its audit entry.
    db.add(AuditLog(org_id=org_id, actor_type="user", actor_id=str(actor.id),
                    actor_role=actor.role, event_type="ADMIN_ACTION", event_category="admin",
                    action=action, entity_type=entity, entity_id=str(entity_id), changes=changes))


async def _organization(db, org_id):
    org = await db.scalar(select(Organization).where(
        Organization.id == org_id, Organization.deleted_at.is_(None)))
    if org is None:
        raise NotFoundError("Organization not found")
    return org


async def create_plan(db, data, actor):
    values = data.model_dump()
    values["limits"] = data.limits.model_dump(exclude_unset=True)
    plan = Plan(**values)
    db.add(plan)
    try:
        await db.flush()
        _audit(db, actor, actor.org_id, "billing.plan_created", "billing_plan", plan.id, values)
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ConflictError("Plan code already exists") from exc
    await db.refresh(plan)
    return plan


async def list_plans(db, offset=0, limit=50):
    return list((await db.scalars(select(Plan).order_by(Plan.code).offset(offset).limit(limit))).all())


async def get_subscription(db, org_id):
    await _organization(db, org_id)
    return await db.scalar(select(Subscription).where(Subscription.org_id == org_id))


async def put_subscription(db, org_id, data, actor):
    await _organization(db, org_id)
    plan = await db.get(Plan, data.plan_id)
    if plan is None:
        raise NotFoundError("Plan not found")
    existing = await db.scalar(select(Subscription).where(Subscription.org_id == org_id))
    # Inactive plans cannot be newly assigned, but existing agreements can be canceled/suspended.
    if not plan.is_active and (existing is None or existing.plan_id != plan.id):
        raise BadRequestError("Cannot assign an inactive plan")
    version = existing.version if existing else 0
    if data.expected_version != version:
        raise ConflictError("Subscription changed; reload and retry with its current version")
    before = SubscriptionResponse.model_validate(existing).model_dump(mode="json") if existing else None
    values = data.model_dump(exclude={"expected_version"})
    values["limit_overrides"] = data.limit_overrides.model_dump(exclude_unset=True)
    for key in ("current_period_start", "current_period_end", "trial_ends_at"):
        if values[key] is not None:
            values[key] = _utc(values[key])
    now = datetime.now(timezone.utc)
    values["canceled_at"] = (existing.canceled_at if existing and existing.status == "canceled" else now) if data.status == "canceled" else None
    values["version"] = version + 1
    values["updated_at"] = now
    try:
        if existing:
            result = await db.execute(update(Subscription).where(
                Subscription.org_id == org_id, Subscription.version == version,
            ).values(**values).execution_options(synchronize_session=False))
            if result.rowcount != 1:
                await db.rollback()
                raise ConflictError("Subscription changed; reload and retry")
            await db.refresh(existing)
        else:
            existing = Subscription(org_id=org_id, **values)
            db.add(existing)
            await db.flush()
            await db.refresh(existing)
        after = SubscriptionResponse.model_validate(existing).model_dump(mode="json")
        _audit(db, actor, org_id, "billing.subscription_updated", "billing_subscription", existing.id,
               {"before": before, "after": after})
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ConflictError("Subscription could not be saved; reload and check its references") from exc
    await db.refresh(existing)
    return existing


def _utc(value):
    # SQLite test storage drops timezone information; application dates are UTC.
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


async def get_entitlements(db, org_id, *, now=None):
    """Resolve persisted plan + contract overrides. This helper does not consume quotas.

    Unconfigured/suspended/expired subscriptions never imply a paid grant. Existing
    product routes are not gated by this helper until a separate enforcement rollout.
    """
    subscription = await get_subscription(db, org_id)
    if subscription is None:
        return EntitlementResponse(org_id=org_id, configured=False, access_allowed=False,
                                   reason="unconfigured", plan_code=None, subscription_status=None,
                                   limits=Limits(), features={})
    plan = await db.get(Plan, subscription.plan_id)
    if plan is None:
        raise NotFoundError("Subscription plan not found")
    limits = {**(plan.limits or {}), **(subscription.limit_overrides or {})}
    features = {**(plan.features or {}), **(subscription.feature_overrides or {})}
    now = _utc(now or datetime.now(timezone.utc))
    reason = "allowed"
    if subscription.status not in {"active", "trialing"}:
        reason = subscription.status
    elif now < _utc(subscription.current_period_start):
        reason = "not_started"
    elif now >= _utc(subscription.current_period_end):
        reason = "period_ended"
    elif subscription.status == "trialing" and (subscription.trial_ends_at is None or now >= _utc(subscription.trial_ends_at)):
        reason = "trial_ended"
    allowed = reason == "allowed"
    return EntitlementResponse(org_id=org_id, configured=True, access_allowed=allowed,
                               reason=reason, plan_code=plan.code, subscription_status=subscription.status,
                               limits=Limits.model_validate(limits),
                               features=features if allowed else {key: False for key in features})


async def get_billing(db, org_id):
    subscription = await get_subscription(db, org_id)
    return BillingResponse(subscription=SubscriptionResponse.model_validate(subscription) if subscription else None,
                           entitlements=await get_entitlements(db, org_id))
