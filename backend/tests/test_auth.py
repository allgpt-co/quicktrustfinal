import uuid

import pytest
from sqlalchemy import select

from app.core import security
from app.core.dependencies import get_current_user
from app.main import app
from app.models.auth import AuthSession
from app.models.user import User
from app.services import auth_service
from tests.conftest import override_get_current_user


@pytest.fixture(autouse=True)
def signing_key(monkeypatch):
    monkeypatch.setattr(security.settings, "SECRET_KEY", "test-signing-key-that-is-long-enough-1234")
    monkeypatch.setattr(security.settings, "JWT_ISSUER", "quicktrust-test")
    monkeypatch.setattr(security.settings, "JWT_AUDIENCE", "quicktrust-test-api")


def test_argon2id_password_hashing_and_policy() -> None:
    encoded = security.hash_password("Correct Horse 9! Battery", "person@example.com")
    assert encoded.startswith("$argon2id$")
    assert security.verify_password("Correct Horse 9! Battery", encoded)
    assert not security.verify_password("wrong password", encoded)
    with pytest.raises(Exception):
        security.hash_password("short", "person@example.com")


@pytest.mark.asyncio
async def test_register_login_refresh_and_protected_me(client) -> None:
    registration = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "owner@example.com",
            "full_name": "Owner Example",
            "password": "Strong Password 9!",
        },
    )
    assert registration.status_code == 201, registration.text
    assert registration.json()["access_token"]
    assert registration.cookies.get("qt_refresh")

    app.dependency_overrides.pop(get_current_user, None)
    try:
        me = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {registration.json()['access_token']}"},
        )
        assert me.status_code == 200, me.text
        assert me.json()["email"] == "owner@example.com"
        assert me.json()["role"] == "super_admin"
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

    wrong = await client.post(
        "/api/v1/auth/token",
        json={"username": "owner@example.com", "password": "Wrong Password 9!"},
    )
    assert wrong.status_code == 401
    assert wrong.json()["detail"] == "Invalid email or password"

    login = await client.post(
        "/api/v1/auth/token",
        json={"username": "owner@example.com", "password": "Strong Password 9!"},
    )
    assert login.status_code == 200, login.text
    old_refresh = login.cookies.get("qt_refresh")
    refreshed = await client.post("/api/v1/auth/refresh")
    assert refreshed.status_code == 200, refreshed.text
    assert refreshed.cookies.get("qt_refresh") != old_refresh


@pytest.mark.asyncio
async def test_refresh_token_is_hashed_and_rotated(db, client) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "hash-check@example.com",
            "full_name": "Hash Check",
            "password": "Another Strong 4! Password",
        },
    )
    raw_token = response.json()["refresh_token"]
    session = (await db.execute(select(AuthSession))).scalars().first()
    assert session is not None
    assert session.refresh_token_hash != raw_token
    assert len(session.refresh_token_hash) == 64


@pytest.mark.asyncio
async def test_existing_user_can_establish_password_with_one_time_reset(db, monkeypatch) -> None:
    from app.models.organization import Organization

    org = Organization(name="Migrated Org", slug=f"migrated-{uuid.uuid4().hex[:8]}")
    db.add(org)
    await db.flush()
    user = User(
        org_id=org.id,
        legacy_identity_id="legacy-subject",
        email="migrated@example.com",
        password_hash=None,
        full_name="Migrated User",
        role="employee",
        is_active=True,
    )
    db.add(user)
    await db.commit()

    captured: dict[str, str] = {}

    async def capture_reset(target, raw_token):
        captured["token"] = raw_token

    monkeypatch.setattr(auth_service, "_send_password_reset_email", capture_reset)
    await auth_service.request_password_reset(db, user.email)
    await auth_service.reset_password(db, captured["token"], "Established Password 7!")
    authenticated = await auth_service.authenticate_user(
        db, user.email, "Established Password 7!"
    )
    assert authenticated.id == user.id

    with pytest.raises(Exception):
        await auth_service.reset_password(db, captured["token"], "Second Password 8!")
