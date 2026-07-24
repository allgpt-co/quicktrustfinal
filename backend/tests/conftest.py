import asyncio
import uuid
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base
from app.core.dependencies import get_db, get_current_user
from app.main import app
from app.models.user import User

# Use a separate test database or SQLite for tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Stable IDs so the test user's org_id matches orgs created via API
TEST_USER_ID = uuid.UUID("aaaaaaaa-aaaa-4aaa-aaaa-aaaaaaaaaaaa")
TEST_ORG_ID = uuid.UUID("bbbbbbbb-bbbb-4bbb-bbbb-bbbbbbbbbbbb")


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        yield session


def make_test_user(org_id: uuid.UUID | None = None) -> User:
    return User(
        id=TEST_USER_ID,
        org_id=org_id or TEST_ORG_ID,
        email="test@quicktrust.dev",
        full_name="Test User",
        role="super_admin",
        is_active=True,
    )


async def override_get_current_user():
    return make_test_user()


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def db():
    async with test_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_org(client):
    resp = await client.post("/api/v1/organizations", json={"name": "Test Org", "slug": "test-org-shared"})
    return resp.json()["id"]


@pytest_asyncio.fixture
async def org_id(client):
    """Create an org and return its ID. Also patches the test user to use this org."""
    resp = await client.post(
        "/api/v1/organizations",
        json={"name": "Fixture Test Org", "slug": "fixture-test-org"},
    )
    created_org_id = resp.json()["id"]

    # Patch the dependency override so the test user belongs to this org
    async def _override():
        return make_test_user(org_id=uuid.UUID(created_org_id))

    app.dependency_overrides[get_current_user] = _override
    yield created_org_id
    # Restore default override
    app.dependency_overrides[get_current_user] = override_get_current_user


@pytest_asyncio.fixture
async def auth_headers():
    """Auth headers stub — authentication is handled by dependency override."""
    return {}


def make_test_user_with_role(role: str, org_id: uuid.UUID | None = None) -> User:
    return User(
        id=uuid.uuid4(),
        org_id=org_id or TEST_ORG_ID,
        email=f"{role}@quicktrust.dev",
        full_name=f"Test {role.title()}",
        role=role,
        is_active=True,
    )
