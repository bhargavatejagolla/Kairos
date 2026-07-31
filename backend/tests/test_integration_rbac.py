from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.api.deps.database import get_db
from app.db.base import Base
from app.main import app

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


from app.api.deps.services import get_authorization_service
from app.services.authorization import AuthorizationService


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    class MockAuthService(AuthorizationService):
        def has_permission(self, context, permission):
            return False

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authorization_service] = lambda: MockAuthService()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_full_authorization_flow(client: AsyncClient, db_session: AsyncSession) -> None:
    # We must seed RBAC roles for the organization creation to work!
    from app.db.seeds.seed_runner import seed_rbac
    await seed_rbac(db_session)

    # 1. Register User
    register_payload = {
        "email": "authz@example.com",
        "username": "authzuser",
        "full_name": "Authz User",
        "password": "productionpassword123",
    }
    res_reg = await client.post("/api/v1/users", json=register_payload)
    assert res_reg.status_code == 201

    # 2. Login
    login_payload = {
        "email": "authz@example.com",
        "password": "productionpassword123",
    }
    res_login = await client.post(
        "/api/v1/auth/login",
        json=login_payload,
    )
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Organization (to get a context)
    org_payload = {"name": "Authz Org", "slug": "authz-org"}
    res_org = await client.post("/api/v1/organizations", json=org_payload, headers=headers)
    assert res_org.status_code == 201

    # 4. Access Protected Endpoint 
    # Because we mocked AuthorizationService to ALWAYS return False for has_permission,
    # even the owner will get a 403 when trying to update the org.
    res_update = await client.patch(
        "/api/v1/organizations/authz-org", json={"name": "New Name"}, headers=headers
    )
    assert res_update.status_code == 403
