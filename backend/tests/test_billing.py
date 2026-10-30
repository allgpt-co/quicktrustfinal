"""QT-008: isolated local tests; no payment/AI credentials or external services."""
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from sqlalchemy import select, func

from app.core.dependencies import get_current_user
from app.main import app
from app.models.audit_log import AuditLog
from app.models.billing import Plan, Subscription
from app.services import billing_service
from tests.conftest import make_test_user_with_role, override_get_current_user, test_session as sessions

PLANS = "/api/v1/admin/billing/plans"


def subscription_url(org_id):
    return f"/api/v1/admin/organizations/{org_id}/subscription"


def read_url(org_id):
    return f"/api/v1/organizations/{org_id}/billing/subscription"


def entitlements_url(org_id):
    return f"/api/v1/organizations/{org_id}/entitlements"


def assignment(plan_id, **overrides):
    now = datetime.now(timezone.utc)
    return dict(plan_id=plan_id, expected_version=0, status="active", billing_interval="month",
                current_period_start=(now - timedelta(days=1)).isoformat(),
                current_period_end=(now + timedelta(days=29)).isoformat(), **overrides)


async def plan(client, **overrides):
    data = {"code": "test_plan", "name": "Test Plan", "limits": {"seats": 5, "documents": 10},
            "features": {"export": True, "sso": False}}
    data.update(overrides)
    result = await client.post(PLANS, json=data)
    assert result.status_code == 201, result.text
    return result.json()


@pytest.fixture(autouse=True)
def restore_auth():
    saved = app.dependency_overrides[get_current_user]
    yield
    app.dependency_overrides[get_current_user] = saved


def login(role, org_id):
    async def user():
        return make_test_user_with_role(role, UUID(org_id))
    app.dependency_overrides[get_current_user] = user


@pytest.mark.asyncio
async def test_unconfigured_org_does_not_gain_paid_features_or_break_settings(client, org_id):
    login("super_admin", org_id)
    response = await client.get(read_url(org_id))
    assert response.status_code == 200
    data = response.json()
    assert data["subscription"] is None
    assert data["entitlements"]["configured"] is False
    assert data["entitlements"]["access_allowed"] is False
    assert data["entitlements"]["reason"] == "unconfigured"
    assert data["entitlements"]["enforcement_enabled"] is False
    assert (await client.get(f"/api/v1/organizations/{org_id}")).status_code == 200


@pytest.mark.asyncio
async def test_assignment_merges_sparse_false_zero_and_null_overrides_and_audits(client, org_id):
    p = await plan(client)
    result = await client.put(subscription_url(org_id), json=assignment(p["id"],
        limit_overrides={"seats": 0, "storage_bytes": None}, feature_overrides={"export": False, "sso": True}))
    assert result.status_code == 200, result.text
    assert result.json()["version"] == 1
    assert result.json()["limit_overrides"] == {"seats": 0, "storage_bytes": None}
    login("super_admin", org_id)
    read = await client.get(read_url(org_id))
    assert read.status_code == 200
    effective = read.json()["entitlements"]
    assert effective["limits"]["seats"] == 0
    assert effective["limits"]["documents"] == 10
    assert effective["limits"]["storage_bytes"] is None
    assert effective["features"] == {"export": False, "sso": True}
    assert effective["access_allowed"] is True
    async with sessions() as db:
        entries = list((await db.scalars(select(AuditLog).where(AuditLog.action == "billing.subscription_updated"))).all())
        assert len(entries) == 1
        assert str(entries[0].org_id) == org_id
        assert entries[0].changes["before"] is None
        assert entries[0].changes["after"]["version"] == 1
        assert (await db.get(Plan, UUID(p["id"]))).features["export"] is True


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["super_admin", "compliance_manager", "employee"])
async def test_customer_cannot_assign_plans_or_read_foreign_tenant(client, org_id, role):
    p = await plan(client)
    foreign = (await client.post("/api/v1/organizations", json={"name": "Other", "slug": "other"})).json()["id"]
    assert (await client.put(subscription_url(foreign), json=assignment(p["id"]))).status_code == 200
    login(role, org_id)
    assert (await client.post(PLANS, json={"code": "escalate", "name": "Escalate"})).status_code == 403
    assert (await client.get(PLANS)).status_code == 403
    assert (await client.put(subscription_url(org_id), json=assignment(p["id"]))).status_code == 403
    assert (await client.put(subscription_url(foreign), json=assignment(p["id"]))).status_code == 403
    assert (await client.get(read_url(foreign))).status_code == 403
    assert (await client.get(entitlements_url(foreign))).status_code == 403
    assert (await client.get(entitlements_url(org_id))).status_code == 200
    assert (await client.get(read_url(org_id))).status_code == (200 if role == "super_admin" else 403)


@pytest.mark.asyncio
async def test_unauthenticated_requests_are_rejected(client, org_id):
    app.dependency_overrides.pop(get_current_user)
    assert (await client.get(read_url(org_id))).status_code == 401
    assert (await client.get(entitlements_url(org_id))).status_code == 401
    assert (await client.get(PLANS)).status_code == 401
    assert (await client.post(PLANS, json={"code": "test", "name": "Test"})).status_code == 401


@pytest.mark.asyncio
async def test_version_conflicts_and_cancellation_preserve_audit(client, org_id):
    p = await plan(client)
    data = assignment(p["id"])
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 200
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 409
    data.update(expected_version=1, status="canceled")
    updated = await client.put(subscription_url(org_id), json=data)
    assert updated.status_code == 200
    assert updated.json()["version"] == 2
    assert updated.json()["canceled_at"] is not None
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 409
    effective = (await client.get(entitlements_url(org_id))).json()
    assert effective["reason"] == "canceled"
    assert effective["features"]["export"] is False
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Subscription)) == 1
        changes = list((await db.scalars(select(AuditLog).where(AuditLog.action == "billing.subscription_updated"))).all())
        assert len(changes) == 2
        assert any(e.changes["before"] and e.changes["before"]["status"] == "active" and e.changes["after"]["status"] == "canceled" for e in changes)


@pytest.mark.asyncio
@pytest.mark.parametrize("change", [
    {"limits": {"seats": -1}}, {"limits": {"seats": True}}, {"limits": {"unknown": 5}},
    {"features": {"sso": "yes"}}, {"features": {"bad key": True}}, {"name": "  "},
])
async def test_plan_input_validation(client, org_id, change):
    data = {"code": "valid", "name": "Valid"} | change
    assert (await client.post(PLANS, json=data)).status_code == 422
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Plan)) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("change", [
    {"status": "paid"}, {"source": "stripe"}, {"limit_overrides": {"seats": -1}},
    {"is_platform_admin": True}, {"status": "trialing"},
    {"current_period_end": "2000-01-01T00:00:00Z"},
    {"current_period_start": "2026-01-01T00:00:00"}, {"expected_version": True},
])
async def test_subscription_validation(client, org_id, change):
    p = await plan(client)
    data = assignment(p["id"]) | change
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 422
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Subscription)) == 0


@pytest.mark.asyncio
async def test_missing_inactive_and_duplicate_plan(client, org_id):
    p = await plan(client, is_active=False)
    assert (await client.put(subscription_url(org_id), json=assignment(p["id"]))).status_code == 400
    assert (await client.put(subscription_url(org_id), json=assignment(str(uuid4())))).status_code == 404
    assert (await client.put(subscription_url(str(uuid4())), json=assignment(p["id"]))).status_code == 404
    assert (await client.post(PLANS, json={"code": p["code"], "name": "Duplicate"})).status_code == 409
    assert len((await client.get(PLANS)).json()) == 1
    assert (await client.get(PLANS + "?limit=1000")).status_code == 422


@pytest.mark.asyncio
@pytest.mark.parametrize("status,reason", [("active", "allowed"), ("trialing", "trial_ended"),
                                         ("past_due", "past_due"), ("suspended", "suspended")])
async def test_entitlements_use_status_and_dates(client, org_id, status, reason):
    p = await plan(client)
    now = datetime.now(timezone.utc)
    data = assignment(p["id"]) | {"status": status}
    if status == "trialing":
        data["trial_ends_at"] = (now - timedelta(hours=1)).isoformat()
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 200
    async with sessions() as db:
        effective = await billing_service.get_entitlements(db, UUID(org_id), now=now)
        assert effective.reason == reason
        assert effective.access_allowed == (reason == "allowed")
        assert effective.features["export"] == effective.access_allowed
        if status == "active":
            assert (await billing_service.get_entitlements(db, UUID(org_id), now=now + timedelta(days=31))).reason == "period_ended"
            assert (await billing_service.get_entitlements(db, UUID(org_id), now=now - timedelta(days=2))).reason == "not_started"


@pytest.mark.asyncio
async def test_org_settings_cannot_grant_entitlements(client, org_id):
    login("super_admin", org_id)
    result = await client.patch(f"/api/v1/organizations/{org_id}", json={"settings": {"plan": "enterprise", "features": {"sso": True}}})
    assert result.status_code == 200
    assert (await client.get(entitlements_url(org_id))).json()["configured"] is False


@pytest.mark.asyncio
async def test_audit_failure_rolls_back_subscription(client, org_id, monkeypatch):
    p = await plan(client)
    from app.schemas.billing import SubscriptionPut
    from tests.conftest import make_test_user
    def fail(*args, **kwargs):
        raise RuntimeError("simulated audit failure")
    monkeypatch.setattr(billing_service, "_audit", fail)
    async with sessions() as db:
        with pytest.raises(RuntimeError, match="audit failure"):
            await billing_service.put_subscription(db, UUID(org_id), SubscriptionPut(**assignment(p["id"])), make_test_user())
        await db.rollback()
    async with sessions() as db:
        assert await db.scalar(select(func.count()).select_from(Subscription)) == 0
