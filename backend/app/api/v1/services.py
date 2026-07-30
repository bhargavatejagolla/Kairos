from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.deps.authorization import require_service_permission
from app.api.deps.project import ProjectContextDep
from app.api.deps.services import get_service_service
from app.core.permissions import Permission
from app.schemas.pagination import PaginatedResponse
from app.schemas.service import ServiceCreate, ServiceResponse
from app.services.service_service import ServiceService

router = APIRouter(tags=["Services"])

@router.post(
    "/organizations/{org_slug}/projects/{project_slug}/services",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_service_permission(Permission.PROJECTS_UPDATE))]
)
async def create_service(
    data: ServiceCreate,
    ctx: ProjectContextDep,
    service_service: Annotated[ServiceService, Depends(get_service_service)]
):
    return await service_service.create(ctx, data, created_by=ctx.member.user_id)

@router.get(
    "/organizations/{org_slug}/projects/{project_slug}/services",
    response_model=PaginatedResponse[ServiceResponse],
    dependencies=[Depends(require_service_permission(Permission.PROJECTS_VIEW))]
)
async def list_services(
    ctx: ProjectContextDep,
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    page: int = 1,
    page_size: int = 50,
):
    # This is a simplified pagination implementation.
    skip = (page - 1) * page_size
    services = await service_service.list_by_project(ctx, skip=skip, limit=page_size)
    # Ideally, we should also query count for full paginated response.
    # For now returning dummy total based on fetched size.
    return PaginatedResponse.create(services, len(services), page, page_size)

