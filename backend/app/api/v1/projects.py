from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.deps.auth import get_current_user
from app.api.deps.organization import OrganizationContextDep, get_organization_context
from app.api.deps.project import ProjectContextDep
from app.api.deps.rbac import RequirePermission
from app.api.deps.services import get_project_service, get_project_settings_service
from app.core.pagination import PaginationParams, get_pagination_params
from app.core.permissions import Permission
from app.core.project import ProjectStatus
from app.schemas.pagination import PaginatedResponse
from app.schemas.project import ProjectCreate, ProjectDetails, ProjectResponse, ProjectUpdate
from app.schemas.project_settings import ProjectSettingsResponse, ProjectSettingsUpdate
from app.services.project_service import ProjectService
from app.services.project_settings_service import ProjectSettingsService

router = APIRouter()


@router.post(
    "",
    response_model=ProjectDetails,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_CREATE))],
    summary="Create a new project",
)
async def create_project(
    org_ctx: OrganizationContextDep,
    data: ProjectCreate,
    user=Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Any:
    return await project_service.create_project(
        organization_id=org_ctx.organization.id,
        user_id=user.id,
        data=data,
    )


@router.get(
    "",
    response_model=PaginatedResponse[ProjectResponse],
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_VIEW))],
    summary="List projects",
)
async def list_projects(
    org_ctx: OrganizationContextDep,
    query: str | None = Query(None, description="Search query"),
    status: ProjectStatus | None = Query(None, description="Filter by status"),
    environment_id: UUID | None = Query(None, description="Filter by environment"),
    pagination: PaginationParams = Depends(get_pagination_params),
    project_service: ProjectService = Depends(get_project_service),
) -> Any:
    projects = await project_service.list_projects(
        organization_id=org_ctx.organization.id,
        query=query,
        status=status,
        environment_id=environment_id,
        skip=pagination.skip,
        limit=pagination.page_size,
    )
    # Ideally, we should fetch total count as well in the service layer, but for simplicity:
    total = len(projects) # Replace with a real count later!
    return PaginatedResponse.create(
        items=projects,
        total=total, # Need to implement proper total count query in repo
        page=pagination.page,
        page_size=pagination.page_size,
    )


@router.get(
    "/{project_slug}",
    response_model=ProjectDetails,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_VIEW))],
    summary="Get project details",
)
async def get_project(project_ctx: ProjectContextDep) -> Any:
    return project_ctx.project


@router.patch(
    "/{project_slug}",
    response_model=ProjectDetails,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_UPDATE))],
    summary="Update a project",
)
async def update_project(
    project_ctx: ProjectContextDep,
    data: ProjectUpdate,
    user=Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Any:
    return await project_service.update_project(
        organization_id=project_ctx.organization.id,
        slug=project_ctx.project.slug,
        user_id=user.id,
        data=data,
    )


@router.post(
    "/{project_slug}/archive",
    response_model=ProjectDetails,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_ARCHIVE))],
    summary="Archive a project",
)
async def archive_project(
    project_ctx: ProjectContextDep,
    user=Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Any:
    return await project_service.archive_project(
        organization_id=project_ctx.organization.id,
        slug=project_ctx.project.slug,
        user_id=user.id,
    )


@router.post(
    "/{project_slug}/restore",
    response_model=ProjectDetails,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_RESTORE))],
    summary="Restore a project",
)
async def restore_project(
    project_ctx: ProjectContextDep,
    user=Depends(get_current_user),
    project_service: ProjectService = Depends(get_project_service),
) -> Any:
    return await project_service.restore_project(
        organization_id=project_ctx.organization.id,
        slug=project_ctx.project.slug,
        user_id=user.id,
    )


@router.get(
    "/{project_slug}/settings",
    response_model=ProjectSettingsResponse,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_VIEW))],
    summary="Get project settings",
)
async def get_project_settings(project_ctx: ProjectContextDep) -> Any:
    return project_ctx.settings


@router.patch(
    "/{project_slug}/settings",
    response_model=ProjectSettingsResponse,
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_SETTINGS_UPDATE))],
    summary="Update project settings",
)
async def update_project_settings(
    project_ctx: ProjectContextDep,
    data: ProjectSettingsUpdate,
    settings_service: ProjectSettingsService = Depends(get_project_settings_service),
) -> Any:
    return await settings_service.update_settings(project_ctx.project.id, data)


@router.get(
    "/{project_slug}/stats",
    dependencies=[Depends(RequirePermission(Permission.PROJECTS_VIEW))],
    summary="Get project statistics",
)
async def get_project_stats(project_ctx: ProjectContextDep) -> Any:
    # Dummy implementation for Phase 8. Will be integrated later.
    return {
        "incidents": 12,
        "alerts": 48,
        "health_score": 96,
        "availability": 99.97,
        "mttr": 15,
        "services": 8,
    }
