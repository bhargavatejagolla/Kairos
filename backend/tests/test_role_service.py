from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.exceptions import (
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from app.db.base import Base
from app.db.models.permission import Permission
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.services.role_service import RoleService

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
def role_service(db_session: AsyncSession) -> RoleService:
    role_repo = RoleRepository(db_session)
    perm_repo = PermissionRepository(db_session)
    return RoleService(role_repository=role_repo, permission_repository=perm_repo)


@pytest.mark.anyio
async def test_create_role(role_service: RoleService) -> None:
    role = await role_service.create_role(
        RoleCreate(name="editor", description="Editor role")
    )
    assert role.id is not None
    assert role.name == "editor"

    # Test duplicate creation
    with pytest.raises(RoleAlreadyExistsError):
        await role_service.create_role(
            RoleCreate(name="editor", description="Another one")
        )


@pytest.mark.anyio
async def test_update_and_delete_role(role_service: RoleService) -> None:
    role = await role_service.create_role(
        RoleCreate(name="publisher", description="Publish stuff")
    )

    updated = await role_service.update_role(
        role.id, RoleUpdate(description="New description")
    )
    assert updated.description == "New description"

    await role_service.delete_role(role.id)

    with pytest.raises(RoleNotFoundError):
        await role_service.get_role(role.id)


@pytest.mark.anyio
async def test_assign_and_remove_permission(
    role_service: RoleService, db_session: AsyncSession
) -> None:
    role = await role_service.create_role(
        RoleCreate(name="moderator", description="Mod role")
    )

    perm = Permission(name="comments:delete", description="Delete comments")
    db_session.add(perm)
    await db_session.commit()
    await db_session.refresh(perm)

    # Assign permission
    updated_role = await role_service.assign_permission(role.id, perm.id)
    assert len(updated_role.permissions) == 1
    assert updated_role.permissions[0].name == "comments:delete"

    # Assigning again should be idempotent
    updated_role = await role_service.assign_permission(role.id, perm.id)
    assert len(updated_role.permissions) == 1

    # Remove permission
    updated_role = await role_service.remove_permission(role.id, perm.id)
    assert len(updated_role.permissions) == 0

    # Removing again should be idempotent
    updated_role = await role_service.remove_permission(role.id, perm.id)
    assert len(updated_role.permissions) == 0
