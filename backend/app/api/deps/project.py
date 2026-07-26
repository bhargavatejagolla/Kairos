from typing import Annotated

from fastapi import Depends, HTTPException, Path, status

from app.api.deps.organization import get_organization_context
from app.api.deps.services import get_project_service
from app.core.organization_context import OrganizationContext
from app.core.project_context import ProjectContext
from app.services.project_service import ProjectService


async def get_project_context(
    project_slug: str = Path(..., description="The slug of the project"),
    org_ctx: OrganizationContext = Depends(get_organization_context),
    project_service: ProjectService = Depends(get_project_service),
) -> ProjectContext:
    try:
        project = await project_service.get_project(org_ctx.organization.id, project_slug)
    except Exception:
        # Assuming ProjectNotFoundError is raised or None is returned
        project = None

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # We expect project to have environment and settings loaded
    return ProjectContext(
        organization=org_ctx.organization,
        member=org_ctx.membership,
        role=org_ctx.role,
        project=project,
        environment=project.environment,
        settings=project.settings,
    )


ProjectContextDep = Annotated[ProjectContext, Depends(get_project_context)]
