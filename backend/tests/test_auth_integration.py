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


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_auth_full_integration_flow(client: AsyncClient) -> None:
    """
    Verify complete e2e authentication lifecycle:
    Register -> Login -> Receive Tokens -> Call /me -> Refresh -> Logout -> Cannot Refresh Again.
    """
    # 1. Register a new user via users API
    register_payload = {
        "email": "integration@example.com",
        "username": "intuser",
        "full_name": "Integration User",
        "password": "productionpassword123",
    }
    res_reg = await client.post("/api/v1/users", json=register_payload)
    assert res_reg.status_code == 201
    user_data = res_reg.json()
    assert user_data["email"] == "integration@example.com"

    # 2. Login
    login_payload = {
        "email": "integration@example.com",
        "password": "productionpassword123",
    }
    res_login = await client.post(
        "/api/v1/auth/login",
        json=login_payload,
        headers={"User-Agent": "KAIROS-Integration-Test/1.0"},
    )
    assert res_login.status_code == 200
    token_data = res_login.json()
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]
    assert access_token is not None
    assert refresh_token is not None

    # 3. Call protected endpoint /me
    res_me = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert res_me.status_code == 200
    me_data = res_me.json()
    assert me_data["user"]["id"] == user_data["id"]
    assert me_data["user"]["email"] == "integration@example.com"

    # 4. Refresh token rotation
    res_refresh = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert res_refresh.status_code == 200
    new_token_data = res_refresh.json()
    new_access_token = new_token_data["access_token"]
    new_refresh_token = new_token_data["refresh_token"]
    assert new_access_token != access_token
    assert new_refresh_token != refresh_token

    # 5. Verify old refresh token is now rotated out and rejected
    res_old_refresh = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )
    assert res_old_refresh.status_code == 401

    # 6. Logout using the active new refresh token
    res_logout = await client.post(
        "/api/v1/auth/logout", json={"refresh_token": new_refresh_token}
    )
    assert res_logout.status_code == 200
    assert res_logout.json()["message"] == "Logged out successfully"

    # 7. Verify cannot refresh again after logout
    res_post_logout_refresh = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": new_refresh_token}
    )
    assert res_post_logout_refresh.status_code == 401
