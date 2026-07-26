from collections.abc import AsyncGenerator
from uuid import uuid4

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


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator[None, None]:
    app.dependency_overrides[get_db] = override_get_db
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.anyio
async def test_users_api_crud_flow() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create User
        payload = {
            "email": "api_user@example.com",
            "username": "apiuser",
            "full_name": "API User",
            "password": "securepassword123",
        }
        response = await client.post("/api/v1/users", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "api_user@example.com"
        assert data["username"] == "apiuser"
        assert "password" not in data
        assert "id" in data
        user_id = data["id"]

        # 2. Test duplicate email creation -> 409
        dup_email_payload = {
            "email": "api_user@example.com",
            "username": "otheruser",
            "full_name": "Other User",
            "password": "securepassword123",
        }
        res_dup = await client.post("/api/v1/users", json=dup_email_payload)
        assert res_dup.status_code == 409
        assert res_dup.json()["success"] is False
        assert "HTTP_409" in res_dup.json()["error"]["code"]

        # 3. Test validation error -> 422
        invalid_payload = {
            "email": "not-an-email",
            "username": "us",  # too short (< 3)
            "full_name": "X",
            "password": "123",  # too short (< 8)
        }
        res_invalid = await client.post("/api/v1/users", json=invalid_payload)
        assert res_invalid.status_code == 422
        assert res_invalid.json()["success"] is False
        assert res_invalid.json()["error"]["code"] == "VALIDATION_ERROR"

        # 4. Get User by ID
        res_get = await client.get(f"/api/v1/users/{user_id}")
        assert res_get.status_code == 200
        assert res_get.json()["id"] == user_id

        # 5. Get User Not Found -> 404
        res_not_found = await client.get(f"/api/v1/users/{uuid4()}")
        assert res_not_found.status_code == 404
        assert res_not_found.json()["success"] is False

        # 6. List Users
        res_list = await client.get("/api/v1/users")
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # 7. Update User
        update_payload = {"full_name": "API User Updated", "is_active": False}
        res_update = await client.patch(f"/api/v1/users/{user_id}", json=update_payload)
        assert res_update.status_code == 200
        assert res_update.json()["full_name"] == "API User Updated"
        assert res_update.json()["is_active"] is False

        # 8. Delete User
        res_delete = await client.delete(f"/api/v1/users/{user_id}")
        assert res_delete.status_code == 204

        # Verify deleted -> 404
        res_get_after = await client.get(f"/api/v1/users/{user_id}")
        assert res_get_after.status_code == 404
