import pytest
from uuid import uuid4

from app.core.exceptions import EnvironmentNotFoundError, ProjectAlreadyExistsError, ProjectArchivedError
from app.core.project import ProjectStatus, ProjectVisibility
from app.repositories.environment import EnvironmentRepository
from app.repositories.project import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService
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
    user = User(email="service@test.com", username="service", full_name="service", hashed_password="pw", is_active=True)
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


async def test_project_service_create(db_session, test_organization, test_user):
    env_repo = EnvironmentRepository(db_session)
    proj_repo = ProjectRepository(db_session)
    service = ProjectService(proj_repo, env_repo, db_session)
    
    from app.db.models.environment import Environment
    env = Environment(organization_id=test_organization.id, name="Prod", slug="prod", color="red")
    env = await env_repo.create(env)
    
    data = ProjectCreate(
        name="Service Test",
        slug="service-test",
        description="test",
        environment_id=env.id,
        visibility=ProjectVisibility.PRIVATE
    )
    
    project = await service.create_project(test_organization.id, test_user.id, data)
    assert project.id is not None
    assert project.settings is not None
    
    # Duplicate should fail
    with pytest.raises(ProjectAlreadyExistsError):
        await service.create_project(test_organization.id, test_user.id, data)


async def test_project_service_archive(db_session, test_organization, test_user):
    env_repo = EnvironmentRepository(db_session)
    proj_repo = ProjectRepository(db_session)
    service = ProjectService(proj_repo, env_repo, db_session)
    
    from app.db.models.environment import Environment
    env = Environment(organization_id=test_organization.id, name="Staging", slug="staging", color="yellow")
    env = await env_repo.create(env)
    data = ProjectCreate(
        name="Archive Test",
        slug="archive-test",
        description="test",
        environment_id=env.id,
        visibility=ProjectVisibility.PRIVATE
    )
    
    project = await service.create_project(test_organization.id, test_user.id, data)
    assert project.status == ProjectStatus.ACTIVE
    
    archived = await service.archive_project(test_organization.id, "archive-test", test_user.id)
    assert archived.status == ProjectStatus.ARCHIVED
    
    # Updating archived should fail
    with pytest.raises(ProjectArchivedError):
        await service.update_project(
            test_organization.id, 
            "archive-test", 
            test_user.id, 
            ProjectUpdate(name="Should fail")
        )
        
    restored = await service.restore_project(test_organization.id, "archive-test", test_user.id)
    assert restored.status == ProjectStatus.ACTIVE
