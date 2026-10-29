"""QT-006: real JWTs must not turn customer admins into platform staff."""
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from app.core import security
from app.core.dependencies import get_current_user
from app.main import app
from app.models.invitation import Invitation
from app.models.user import User
from app.services import invitation_service
from tests.conftest import override_get_current_user


@pytest.fixture(autouse=True)
def real_auth(monkeypatch):
    monkeypatch.setattr(security.settings, "SECRET_KEY", "qt006-test-signing-key-at-least-32-characters")
    app.dependency_overrides.pop(get_current_user, None)
    # These tests must never send email or be affected by shared test rate limits.
    from app.core.rate_limit import limiter
    monkeypatch.setattr(limiter, "enabled", False)
    from unittest.mock import AsyncMock
    monkeypatch.setattr(invitation_service, "_send_invitation_email", AsyncMock())
    yield
    app.dependency_overrides[get_current_user] = override_get_current_user


async def register(client, email, **extra):
    response = await client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Tenant test", "password": "Strong Test Password 9!", **extra,
    })
    assert response.status_code == 201, response.text
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    me = await client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    return me.json(), headers


@pytest.mark.asyncio
async def test_signup_admin_is_scoped_for_jwt_and_api_key(client, db):
    a, ha = await register(client, "tenant-a@example.com")
    b, hb = await register(client, "tenant-b@example.com")
    owner = await db.get(User, uuid.UUID(b["id"]))
    assert owner.role == "super_admin"  # retained legacy organization-admin name
    assert owner.is_platform_admin is False
    own = f"/api/v1/organizations/{b['org_id']}"
    foreign = f"/api/v1/organizations/{a['org_id']}"
    assert (await client.get(own + "/users", headers=hb)).status_code == 200
    assert (await client.patch(own, headers=hb, json={"name": "Updated own org"})).status_code == 200
    for method, path, payload in [
        ("GET", foreign + "/users", None),
        ("GET", foreign, None),
        ("PATCH", foreign, {"name": "Unauthorized change"}),
        ("POST", foreign + "/invitations", {"email": "intruder@example.com", "role": "employee"}),
        ("PATCH", foreign + "/users/" + a["id"], {"role": "employee"}),
        ("DELETE", foreign + "/users/" + a["id"], None),
        ("GET", "/api/v1/tenants", None),
        ("GET", f"/api/v1/tenants/{a['org_id']}/isolation-check", None),
        ("POST", "/api/v1/tenants/provision", {"name": "Forbidden tenant"}),
        ("POST", "/api/v1/organizations", {"name": "Forbidden", "slug": "forbidden"}),
        ("POST", "/api/v1/frameworks", {}),
    ]:
        response = await client.request(method, path, headers=hb, json=payload)
        assert response.status_code == 403, (path, response.text)
    key = await client.post(own + "/api-keys", headers=hb, json={"name": "Test"})
    assert key.status_code == 201, key.text
    key_headers = {"X-API-Key": key.json()["key"]}
    assert (await client.get(own + "/users", headers=key_headers)).status_code == 200
    assert (await client.get(foreign + "/users", headers=key_headers)).status_code == 403
    assert (await client.get("/api/v1/tenants", headers=key_headers)).status_code == 403
    # Explicit database provisioning permits platform access; revocation takes effect
    # on the SAME JWT because permissions are loaded from the database per request.
    owner.is_platform_admin = True
    await db.commit()
    assert (await client.get(foreign + "/users", headers=hb)).status_code == 200
    assert (await client.get("/api/v1/tenants", headers=hb)).status_code == 200
    owner.is_platform_admin = False
    await db.commit()
    assert (await client.get(foreign + "/users", headers=hb)).status_code == 403


@pytest.mark.asyncio
async def test_platform_flag_cannot_be_assigned_via_customer_apis(client, db):
    response = await client.post("/api/v1/auth/register", json={
        "email": "spoof@example.com", "full_name": "Spoof", "password": "Strong Password 9!",
        "is_platform_admin": True,
    })
    assert response.status_code == 422
    owner, headers = await register(client, "owner@example.com")
    base = f"/api/v1/organizations/{owner['org_id']}"
    for path, method, body in [
        ("/users", "POST", {"email": "new@example.com", "full_name": "New", "is_platform_admin": True}),
        ("/users/" + owner["id"], "PATCH", {"is_platform_admin": True}),
        ("/invitations", "POST", {"email": "invite@example.com", "role": "super_admin", "is_platform_admin": True}),
        ("/invitations", "POST", {"email": "invite@example.com", "role": "platform_admin"}),
    ]:
        assert (await client.request(method, base + path, headers=headers, json=body)).status_code == 422
    # Even a legitimate invitation to an organization-admin role cannot grant platform access.
    invite = await client.post(base + "/invitations", headers=headers,
                              json={"email": "invited@example.com", "role": "super_admin"})
    assert invite.status_code == 201, invite.text
    member, member_headers = await register(client, "invited@example.com", invitation_token=invite.json()["token"])
    invited = await db.get(User, uuid.UUID(member["id"]))
    assert invited.org_id == uuid.UUID(owner["org_id"])
    assert invited.is_platform_admin is False
    assert (await client.get("/api/v1/tenants", headers=member_headers)).status_code == 403


@pytest.mark.asyncio
async def test_manager_cannot_grant_admin_or_reuse_legacy_privileged_invite(client, db):
    manager_info, headers = await register(client, "manager@example.com")
    manager = await db.get(User, uuid.UUID(manager_info["id"]))
    manager.role = "compliance_manager"
    await db.commit()
    base = f"/api/v1/organizations/{manager.org_id}"
    response = await client.post(base + "/invitations", headers=headers,
                                json={"email": "escalate@example.com", "role": "super_admin"})
    assert response.status_code == 403
    response = await client.post(base + "/invitations", headers=headers,
                                json={"email": "employee@example.com", "role": "employee"})
    assert response.status_code == 201
    employee, employee_headers = await register(
        client, "employee@example.com", invitation_token=response.json()["token"]
    )
    assert employee["role"] == "employee"
    assert (await client.get(base + "/users", headers=employee_headers)).status_code == 403
    assert (await client.post(base + "/invitations", headers=employee_headers,
                             json={"email": "another@example.com", "role": "employee"})).status_code == 403
    # Previously issued admin invites must also be checked at acceptance/registration.
    token = uuid.uuid4().hex
    db.add(Invitation(org_id=manager.org_id, invited_by=manager.id, email="legacy@example.com",
                      role="super_admin", token=token, status="pending",
                      expires_at=datetime.now(timezone.utc) + timedelta(days=1)))
    await db.commit()
    response = await client.post("/api/v1/auth/register", json={
        "email": "legacy@example.com", "full_name": "Legacy", "password": "Strong Password 9!",
        "invitation_token": token,
    })
    assert response.status_code == 403
    assert (await db.execute(select(User).where(User.email == "legacy@example.com"))).scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_customer_cannot_modify_platform_staff_account(client, db):
    owner, headers = await register(client, "customer@example.com")
    staff = User(org_id=uuid.UUID(owner["org_id"]), email="staff@example.com", full_name="Staff",
                 role="super_admin", is_platform_admin=True, is_active=True)
    db.add(staff)
    await db.commit()
    base = f"/api/v1/organizations/{owner['org_id']}/users/{staff.id}"
    for method, path, body in [
        ("PATCH", base, {"is_active": False}), ("DELETE", base, None),
        ("POST", "/api/v1/profile" + base.removeprefix("/api/v1") + "/suspend", {}),
        ("POST", "/api/v1/profile" + base.removeprefix("/api/v1") + "/reactivate", {}),
    ]:
        assert (await client.request(method, path, headers=headers, json=body)).status_code == 403
