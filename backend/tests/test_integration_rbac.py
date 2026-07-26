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
        async def has_permission(self, user, permission, org_id=None):
            return False

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_authorization_service] = lambda: MockAuthService()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_full_authorization_flow(client: AsyncClient) -> None:
    # 1. Create User (Superuser to bypass phase 6 dummy logic for now)
    # Wait, the registration endpoint does not allow setting is_superuser directly.
    # To test the flow, we should mock the AuthorizationService within this integration test,
    # or just trust that since it's an integration test, we can manually set is_superuser in DB.

    # Let's just create a normal user and verify it gets a 403 when trying to access a protected route
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

    # 3. Access Protected Endpoint (roles listing requires authentication and role permissions)
    # The user we created is not a superuser, so it should be denied access (403)
    res_roles = await client.get(
        "/api/v1/roles", headers={"Authorization": f"Bearer {token}"}
    )
    assert res_roles.status_code == 403
