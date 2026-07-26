from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models.user import User
from app.repositories.user import UserRepository

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


@pytest.mark.anyio
async def test_user_repository_crud(db_session: AsyncSession) -> None:
    repo = UserRepository(db_session)

    # Create
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password="hashed_pw_123",
        is_active=True,
    )
    created = await repo.create(user)
    assert created.id is not None
    assert created.email == "test@example.com"
    assert created.username == "testuser"

    # Get by id
    fetched_id = await repo.get_by_id(created.id)
    assert fetched_id is not None
    assert fetched_id.email == "test@example.com"

    # Get by email & exists
    fetched_email = await repo.get_by_email("test@example.com")
    assert fetched_email is not None
    assert await repo.email_exists("test@example.com") is True
    assert await repo.email_exists("nonexistent@example.com") is False

    # Get by username & exists
    fetched_username = await repo.get_by_username("testuser")
    assert fetched_username is not None
    assert await repo.username_exists("testuser") is True
    assert await repo.username_exists("nonexistent") is False

    # List & count
    all_users = await repo.list()
    assert len(all_users) == 1
    assert await repo.count() == 1

    # Update
    created.full_name = "Updated Name"
    updated = await repo.update(created)
    assert updated.full_name == "Updated Name"

    # Exists & Delete
    assert await repo.exists(created.id) is True
    deleted = await repo.delete(created.id)
    assert deleted is True
    assert await repo.exists(created.id) is False
    assert await repo.count() == 0
