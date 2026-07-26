from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
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
    
    # We must seed RBAC roles for the organization creation to work!
    from app.db.seeds.seed_runner import seed_rbac
    async with TestingSessionLocal() as session:
        await seed_rbac(session)

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.anyio
async def test_organization_api_flow() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register User A
        res_a = await client.post(
            "/api/v1/users", 
            json={"email": "a@example.com", "username": "usera", "full_name": "User A", "password": "supersecretpassword"}
        )
        assert res_a.status_code == 201

        # 2. Login User A
        res_login_a = await client.post("/api/v1/auth/login", json={"email": "a@example.com", "password": "supersecretpassword"})
        token_a = res_login_a.json()["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        # 3. Create Organization as User A
        org_payload = {"name": "Test Org", "slug": "test-org"}
        res_org = await client.post("/api/v1/organizations", json=org_payload, headers=headers_a)
        assert res_org.status_code == 201
        org_data = res_org.json()
        assert org_data["slug"] == "test-org"

        # 4. List Organizations
        res_list = await client.get("/api/v1/organizations", headers=headers_a)
        assert res_list.status_code == 200
        assert len(res_list.json()) == 1

        # 5. Register and Login User B
        await client.post("/api/v1/users", json={"email": "b@example.com", "username": "userb", "full_name": "User B", "password": "supersecretpassword"})
        res_login_b = await client.post("/api/v1/auth/login", json={"email": "b@example.com", "password": "supersecretpassword"})
        token_b = res_login_b.json()["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # 6. User B tries to get organization -> 403 Forbidden (not a member)
        res_get_b = await client.get("/api/v1/organizations/test-org", headers=headers_b)
        assert res_get_b.status_code == 403

        # 7. User A (Owner) adds User B as Admin
        # Get Admin role ID first
        async with TestingSessionLocal() as session:
            from app.db.models.role import Role
            from app.db.models.user import User
            from sqlalchemy import select
            admin_role = (await session.execute(select(Role).where(Role.name == "admin"))).scalar_one()
            admin_role_id = str(admin_role.id)
            user_b = (await session.execute(select(User).where(User.email == "b@example.com"))).scalar_one()
            user_b_id = str(user_b.id)

        add_member_payload = {"user_id": user_b_id, "role_id": admin_role_id}
        res_add = await client.post("/api/v1/organizations/test-org/members", json=add_member_payload, headers=headers_a)
        assert res_add.status_code == 201

        # 8. User B gets organization -> 200 OK (now a member)
        res_get_b2 = await client.get("/api/v1/organizations/test-org", headers=headers_b)
        assert res_get_b2.status_code == 200

        # 9. List members
        res_members = await client.get("/api/v1/organizations/test-org/members", headers=headers_a)
        assert res_members.status_code == 200
        assert len(res_members.json()) == 2

        # 10. Update Organization (User A)
        res_update = await client.patch("/api/v1/organizations/test-org", json={"name": "Updated Org"}, headers=headers_a)
        assert res_update.status_code == 200
        assert res_update.json()["name"] == "Updated Org"

        # 11. User B leaves organization
        res_leave = await client.post("/api/v1/organizations/test-org/leave", headers=headers_b)
        assert res_leave.status_code == 204

        # 12. Delete Organization (User A)
        res_del = await client.delete("/api/v1/organizations/test-org", headers=headers_a)
        assert res_del.status_code == 204
