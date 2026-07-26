import pytest
from uuid import uuid4

from app.core.project import ProjectStatus, ProjectVisibility
from app.db.models.environment import Environment
from app.db.models.project import Project
from app.repositories.environment import EnvironmentRepository
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from collections.abc import AsyncGenerator
from app.db.models.user import User
from app.db.models.organization import Organization

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
async def test_user(db_session: AsyncSession) -> User:
    user = User(email="repo@test.com", username="repo", full_name="repo", hashed_password="pw", is_active=True)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
async def test_organization(db_session: AsyncSession, test_user: User) -> Organization:
    org = Organization(name="Test Org", slug="test-org", created_by_id=test_user.id)
    db_session.add(org)
    await db_session.commit()
    await db_session.refresh(org)
    return org

pytestmark = pytest.mark.anyio


async def test_environment_repository(db_session, test_organization):
    repo = EnvironmentRepository(db_session)
    
    # Create
    env = Environment(organization_id=test_organization.id, name="Test Env", slug="test-env", color="blue")
    env = await repo.create(env)
    assert env.id is not None
    assert env.name == "Test Env"
    
    # Get by slug
    fetched = await repo.get_by_slug(test_organization.id, "test-env")
    assert fetched.id == env.id
    
    # Exists
    exists = await repo.exists(test_organization.id, "test-env")
    assert exists is True


async def test_project_repository(db_session, test_organization, test_user):
    env_repo = EnvironmentRepository(db_session)
    proj_repo = ProjectRepository(db_session)
    
    env = Environment(organization_id=test_organization.id, name="Prod", slug="prod", color="red")
    env = await env_repo.create(env)
    
    # Create Project
    project = Project(
        organization_id=test_organization.id,
        environment_id=env.id,
        created_by_id=test_user.id,
        updated_by_id=test_user.id,
        name="Test Project",
        slug="test-proj",
        description="A test project",
        status=ProjectStatus.ACTIVE,
        visibility=ProjectVisibility.PRIVATE
    )
    project = await proj_repo.create(project)
    
    assert project.id is not None
    assert project.name == "Test Project"
    
    # Exists
    assert await proj_repo.exists(test_organization.id, "test-proj")
    
    # Get by slug
    fetched = await proj_repo.get_by_slug(test_organization.id, "test-proj")
    assert fetched.id == project.id
    
    # Search
    results = await proj_repo.search(test_organization.id, query="Test")
    assert len(results) == 1
    assert results[0].slug == "test-proj"
    
    # Update
    project.name = "Updated Name"
    updated = await proj_repo.update(project)
    assert updated.name == "Updated Name"
