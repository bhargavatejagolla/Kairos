from uuid import UUID

from app.core.exceptions import (
    PermissionNotFoundError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)
from app.db.models.role import Role
from app.repositories.permission import PermissionRepository
from app.repositories.role import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    def __init__(
        self,
        role_repository: RoleRepository,
        permission_repository: PermissionRepository,
    ):
        self.roles = role_repository
        self.permissions = permission_repository

    async def create_role(self, data: RoleCreate) -> Role:
        existing = await self.roles.get_by_name(data.name)
        if existing:
            raise RoleAlreadyExistsError()

        role = Role(name=data.name, description=data.description)
        return await self.roles.create(role)

    async def list_roles(self) -> list[Role]:
        return await self.roles.list_roles()

    async def get_role(self, role_id: UUID) -> Role:
        role = await self.roles.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()
        return role

    async def update_role(self, role_id: UUID, data: RoleUpdate) -> Role:
        role = await self.roles.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()

        if data.description is not None:
            role.description = data.description

        return await self.roles.save(role)

    async def delete_role(self, role_id: UUID) -> None:
        role = await self.roles.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()

        await self.roles.delete(role)

    async def assign_permission(self, role_id: UUID, permission_id: UUID) -> Role:
        role = await self.roles.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()

        permission = await self.permissions.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundError()

        if permission not in role.permissions:
            role.permissions.append(permission)
            await self.roles.save(role)

        return role

    async def remove_permission(self, role_id: UUID, permission_id: UUID) -> Role:
        role = await self.roles.get_by_id(role_id)
        if role is None:
            raise RoleNotFoundError()

        permission = await self.permissions.get_by_id(permission_id)
        if permission is None:
            raise PermissionNotFoundError()

        if permission in role.permissions:
            role.permissions.remove(permission)
            await self.roles.save(role)

        return role
