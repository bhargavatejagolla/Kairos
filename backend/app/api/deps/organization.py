from typing import Annotated

from fastapi import Depends, Path

from app.api.deps.auth import ActiveUserDep
from app.api.deps.services import get_organization_service
from app.core.exceptions import OrganizationNotFoundError, PermissionDeniedError
from app.core.organization_context import OrganizationContext
from app.db.models.user import User
from app.services.organization_service import OrganizationService


async def get_organization_context(
    current_user: ActiveUserDep,
    org_service: Annotated[OrganizationService, Depends(get_organization_service)],
    slug: str = Path(..., description="The slug of the organization"),
) -> OrganizationContext:
    org = await org_service.org_repo.get_by_slug(slug)
    if not org:
        raise OrganizationNotFoundError()
        
    member = await org_service.membership_service.membership_repo.get_member(
        org.id, current_user.id
    )
    if not member:
        raise PermissionDeniedError("You are not a member of this organization")
        
    return OrganizationContext(organization=org, membership=member)


OrganizationContextDep = Annotated[OrganizationContext, Depends(get_organization_context)]
