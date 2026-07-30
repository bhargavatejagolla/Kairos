from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.organization import OrganizationStatus
from app.db.base import Base
from app.db.models.organization import Organization
from app.db.models.user import User
from app.repositories.organization import OrganizationRepository

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
async def user(db_session: AsyncSession) -> User:
    user = User(
        email="testorg@example.com",
        username="testorg",
        full_name="Test Org User",
        hashed_password="pw",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.anyio
async def test_organization_repository_create_and_get(db_session, user):
    repo = OrganizationRepository(db_session)
    
    org = Organization(
        name="Test Org",
        slug="test-org",
        description="A test organization",
        created_by_id=user.id
    )
    
    created_org = await repo.create(org)
    assert created_org.id is not None
    assert created_org.name == "Test Org"
    assert created_org.slug == "test-org"
    assert created_org.status == OrganizationStatus.ACTIVE
    
    # Test get_by_id
    fetched_org = await repo.get_by_id(created_org.id)
    assert fetched_org is not None
    assert fetched_org.id == created_org.id
    
    # Test get_by_slug
    fetched_org_slug = await repo.get_by_slug("test-org")
    assert fetched_org_slug is not None
    assert fetched_org_slug.id == created_org.id
    
    # Test exists_slug
    assert await repo.exists_slug("test-org") is True
    assert await repo.exists_slug("non-existent-slug") is False
