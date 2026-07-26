from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.auth import ActiveUserDep
from app.api.deps.database import get_db
from app.core.exceptions import PermissionNotFoundError
from app.repositories.permission import PermissionRepository
from app.schemas.role import PermissionResponse

router = APIRouter(tags=["permissions"])


@router.get(
    "",
    response_model=list[PermissionResponse],
    summary="List all permissions",
)
async def list_permissions(
    current_user: ActiveUserDep,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PermissionResponse]:
    # TODO: Wrap this in a PermissionService later if needed,
    # but since permissions are static, a repo call is fine.
    repo = PermissionRepository(db)
    return await repo.list_permissions()


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Get permission details",
)
async def get_permission(
    permission_id: UUID,
    current_user: ActiveUserDep,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PermissionResponse:
    repo = PermissionRepository(db)
    perm = await repo.get_by_id(permission_id)
    if not perm:
        raise PermissionNotFoundError()
    return perm
