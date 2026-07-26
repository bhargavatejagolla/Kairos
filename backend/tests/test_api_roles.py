from collections.abc import AsyncGenerator
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api.deps.auth import get_current_active_user
from app.api.deps.database import get_db
from app.db.base import Base
from app.db.models.user import User
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
async def auth_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    async def override_get_user() -> User:
        return User(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            email="test@example.com",
            is_active=True,
        )

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_user

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_crud_roles(
    auth_client: AsyncClient,
) -> None:
    # 1. Create a Role
    create_payload = {"name": "custom_role", "description": "A custom role"}
    response = await auth_client.post("/api/v1/roles", json=create_payload)
    assert response.status_code == 201

    role = response.json()
    assert role["name"] == "custom_role"
    assert role["description"] == "A custom role"
    assert "id" in role

    role_id = role["id"]

    # 2. Get the Role
    get_response = await auth_client.get(f"/api/v1/roles/{role_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "custom_role"

    # 3. List Roles
    list_response = await auth_client.get("/api/v1/roles")
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
    assert any(r["name"] == "custom_role" for r in list_response.json())

    # 4. Update the Role
    update_payload = {"description": "Updated description"}
    update_response = await auth_client.patch(
        f"/api/v1/roles/{role_id}", json=update_payload
    )
    assert update_response.status_code == 200
    assert update_response.json()["description"] == "Updated description"

    # 5. Delete the Role
    delete_response = await auth_client.delete(f"/api/v1/roles/{role_id}")
    assert delete_response.status_code == 204

    # 6. Verify Deletion
    verify_response = await auth_client.get(f"/api/v1/roles/{role_id}")
    assert verify_response.status_code == 404


@pytest.mark.anyio
async def test_role_assign_and_remove_permission(
    auth_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    from app.db.models.permission import Permission

    perm = Permission(name="test:permission:role", description="Test perm")
    db_session.add(perm)
    await db_session.commit()
    await db_session.refresh(perm)

    # 1. Create a Role
    response = await auth_client.post("/api/v1/roles", json={"name": "test_perm_role"})
    assert response.status_code == 201
    role_id = response.json()["id"]

    # 2. Get a valid permission to assign
    perms_response = await auth_client.get("/api/v1/permissions")
    assert perms_response.status_code == 200
    perms = perms_response.json()
    assert len(perms) > 0
    perm_id = perms[0]["id"]

    # 3. Assign the permission
    assign_payload = {"permission_id": perm_id}
    assign_response = await auth_client.post(
        f"/api/v1/roles/{role_id}/permissions", json=assign_payload
    )
    assert assign_response.status_code == 200
    updated_role = assign_response.json()
    assert len(updated_role["permissions"]) == 1
    assert updated_role["permissions"][0]["id"] == perm_id

    # 4. Remove the permission
    remove_response = await auth_client.delete(
        f"/api/v1/roles/{role_id}/permissions/{perm_id}"
    )
    assert remove_response.status_code == 200
    cleared_role = remove_response.json()
    assert len(cleared_role["permissions"]) == 0
