from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps.auth import ActiveUserDep
from app.api.deps.rbac import require_permission
from app.api.deps.services import get_role_service
from app.core.permissions import Permission
from app.schemas.role import (
    AssignPermissionRequest,
    RoleCreate,
    RoleResponse,
    RoleUpdate,
)
from app.services.role_service import RoleService

router = APIRouter(tags=["roles"])

RequireRolesRead = Depends(require_permission(Permission.USERS_READ.value))
RequireRolesWrite = Depends(require_permission(Permission.USERS_UPDATE.value))
# TODO: Once we have finer-grained permissions for roles themselves, update these.


@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role",
)
async def create_role(
    data: RoleCreate,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesWrite],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    # TODO: In Phase 7, restrict this to Super Admins or Org Owners
    return await role_service.create_role(data)


@router.get(
    "",
    response_model=list[RoleResponse],
    summary="List all roles",
)
async def list_roles(
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesRead],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> list[RoleResponse]:
    return await role_service.list_roles()


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Get role details",
)
async def get_role(
    role_id: UUID,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesRead],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    return await role_service.get_role(role_id)


@router.patch(
    "/{role_id}",
    response_model=RoleResponse,
    summary="Update a role",
)
async def update_role(
    role_id: UUID,
    data: RoleUpdate,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesWrite],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    # TODO: In Phase 7, restrict this
    return await role_service.update_role(role_id, data)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a role",
)
async def delete_role(
    role_id: UUID,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesWrite],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> None:
    # TODO: In Phase 7, restrict this
    await role_service.delete_role(role_id)


@router.post(
    "/{role_id}/permissions",
    response_model=RoleResponse,
    summary="Assign a permission to a role",
)
async def assign_permission(
    role_id: UUID,
    data: AssignPermissionRequest,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesWrite],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    # TODO: In Phase 7, restrict this
    return await role_service.assign_permission(role_id, data.permission_id)


@router.delete(
    "/{role_id}/permissions/{permission_id}",
    response_model=RoleResponse,
    summary="Remove a permission from a role",
)
async def remove_permission(
    role_id: UUID,
    permission_id: UUID,
    current_user: ActiveUserDep,
    _: Annotated[None, RequireRolesWrite],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> RoleResponse:
    # TODO: In Phase 7, restrict this
    return await role_service.remove_permission(role_id, permission_id)
