from collections.abc import AsyncGenerator

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
        from uuid import UUID

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
async def test_list_permissions(
    auth_client: AsyncClient,
    db_session: AsyncSession,
) -> None:
    from app.db.models.permission import Permission

    perm = Permission(name="test:permission", description="Test perm")
    db_session.add(perm)
    await db_session.commit()
    await db_session.refresh(perm)

    response = await auth_client.get("/api/v1/permissions")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]

    first_perm = data[0]

    # Test get permission by ID
    get_response = await auth_client.get(f"/api/v1/permissions/{first_perm['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == first_perm["name"]


@pytest.mark.anyio
async def test_get_permission_not_found(
    auth_client: AsyncClient,
) -> None:
    from uuid import uuid4

    response = await auth_client.get(f"/api/v1/permissions/{uuid4()}")
    assert response.status_code == 404
