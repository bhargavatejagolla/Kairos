from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.models.permission import Permission
from app.db.models.role import Role
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository

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
async def test_role_create_and_get(db_session: AsyncSession) -> None:
    role_repo = RoleRepository(db_session)

    new_role = Role(name="test_role", description="A test role")
    role = await role_repo.create(new_role)

    assert role.id is not None
    assert role.name == "test_role"
    assert role.description == "A test role"
    assert len(role.permissions) == 0

    fetched_role = await role_repo.get_by_id(role.id)
    assert fetched_role is not None
    assert fetched_role.name == "test_role"


@pytest.mark.anyio
async def test_permission_get_and_list(db_session: AsyncSession) -> None:
    perm_repo = PermissionRepository(db_session)

    # Let's create a permission manually to test
    perm1 = Permission(name="test:read", description="Read test")
    perm2 = Permission(name="test:write", description="Write test")
    db_session.add(perm1)
    db_session.add(perm2)
    await db_session.commit()
    await db_session.refresh(perm1)

    fetched_perm = await perm_repo.get_by_name("test:read")
    assert fetched_perm is not None
    assert fetched_perm.name == "test:read"
    assert fetched_perm.id == perm1.id

    fetched_by_id = await perm_repo.get_by_id(perm1.id)
    assert fetched_by_id is not None
    assert fetched_by_id.name == "test:read"

    perms = await perm_repo.list_permissions()
    assert len(perms) >= 2


@pytest.mark.anyio
async def test_role_assign_permission(db_session: AsyncSession) -> None:
    role_repo = RoleRepository(db_session)
    role = Role(name="manager", description="Manager role")
    await role_repo.create(role)

    perm = Permission(name="manage:users", description="Manage users")
    db_session.add(perm)
    await db_session.commit()
    await db_session.refresh(perm)

    role.permissions.append(perm)
    saved_role = await role_repo.save(role)

    assert len(saved_role.permissions) == 1
    assert saved_role.permissions[0].name == "manage:users"

    fetched_role = await role_repo.get_by_id(role.id)
    assert fetched_role is not None
    assert len(fetched_role.permissions) == 1
    assert fetched_role.permissions[0].name == "manage:users"
