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
    
    from app.db.seeds.rbac import seed_rbac
    async with TestingSessionLocal() as session:
        await seed_rbac(session)

    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.mark.anyio
async def test_project_api_flow() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register User
        await client.post(
            "/api/v1/users", 
            json={"email": "p@example.com", "username": "userp", "full_name": "User P", "password": "supersecretpassword"}
        )
        # Login
        res_login = await client.post("/api/v1/auth/login", json={"email": "p@example.com", "password": "supersecretpassword"})
        token = res_login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create Organization
        res_org = await client.post(
            "/api/v1/organizations",
            headers=headers,
            json={"name": "Project Org", "slug": "project-org"}
        )
        assert res_org.status_code == 201

        # We must insert an environment directly since we don't have an Environment API yet
        async with TestingSessionLocal() as session:
            from app.db.models.environment import Environment
            import uuid
            org_id = uuid.UUID(res_org.json()["id"])
            env = Environment(id=uuid.uuid4(), organization_id=org_id, name="Dev", slug="dev", color="green")
            session.add(env)
            await session.commit()
            await session.refresh(env)
            env_id = str(env.id)

        # Create Project
        payload = {
            "name": "API Test Project",
            "slug": "api-test",
            "description": "Test",
            "environment_id": env_id,
            "visibility": "private"
        }
        res_proj = await client.post(
            "/api/v1/organizations/project-org/projects",
            headers=headers,
            json=payload
        )
        if res_proj.status_code != 201:
            print("ERROR CREATING PROJECT:", res_proj.text)
        assert res_proj.status_code == 201
        
        # List Projects
        res_list = await client.get("/api/v1/organizations/project-org/projects", headers=headers)
        assert res_list.status_code == 200
        assert len(res_list.json()["items"]) == 1

        # Get Project Details
        res_get = await client.get("/api/v1/organizations/project-org/projects/api-test", headers=headers)
        assert res_get.status_code == 200

        # Archive Project
        res_archive = await client.post("/api/v1/organizations/project-org/projects/api-test/archive", headers=headers)
        assert res_archive.status_code == 200

        # Restore Project
        res_restore = await client.post("/api/v1/organizations/project-org/projects/api-test/restore", headers=headers)
        assert res_restore.status_code == 200
