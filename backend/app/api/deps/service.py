from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.project import get_project_context
from app.api.deps.services import get_service_service
from app.core.project_context import ProjectContext
from app.core.service_context import ServiceContext
from app.services.service_service import ServiceService

async def get_service_context(
    service_slug: str = Path(..., description="The slug of the service"),
    project_ctx: ProjectContext = Depends(get_project_context),
    service_service: ServiceService = Depends(get_service_service),
) -> ServiceContext:
    try:
        service = await service_service.repository.get_by_slug(
            organization_id=project_ctx.organization.id,
            project_id=project_ctx.project.id,
            slug=service_slug,
        )
    except Exception:
        service = None

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )

    return ServiceContext(
        organization=project_ctx.organization,
        member=project_ctx.member,
        role=project_ctx.role,
        project=project_ctx.project,
        environment=project_ctx.environment,
        settings=project_ctx.settings,
        service=service,
    )

ServiceContextDep = Annotated[ServiceContext, Depends(get_service_context)]
