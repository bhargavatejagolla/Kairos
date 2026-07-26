from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps.auth import ActiveUserDep
from app.api.deps.organization import OrganizationContextDep
from app.api.deps.rbac import require_permission
from app.api.deps.services import get_membership_service, get_organization_service
from app.schemas.organization import (
    AddMemberRequest,
    ChangeMemberRoleRequest,
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate,
)
from app.schemas.user import UserResponse
from app.services.membership_service import MembershipService
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization(
    data: OrganizationCreate,
    current_user: ActiveUserDep,
    org_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationResponse:
    """Create a new organization and assign the creator as the Owner."""
    org = await org_service.create_organization(data, current_user.id)
    return org


@router.get(
    "",
    response_model=list[OrganizationResponse],
)
async def list_organizations(
    current_user: ActiveUserDep,
    org_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> list[OrganizationResponse]:
    """List all organizations (future: filter by user membership)."""
    # Note: In a real system, you'd filter by user memberships here.
    return await org_service.list_organizations()


@router.get(
    "/{slug}",
    response_model=OrganizationResponse,
)
async def get_organization(
    ctx: OrganizationContextDep,
) -> OrganizationResponse:
    """Get an organization by slug."""
    return ctx.organization


@router.patch(
    "/{slug}",
    response_model=OrganizationResponse,
    dependencies=[Depends(require_permission("organizations:update"))],
)
async def update_organization(
    ctx: OrganizationContextDep,
    data: OrganizationUpdate,
    org_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> OrganizationResponse:
    """Update an organization's details."""
    return await org_service.update_organization(ctx.organization.id, data)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("organizations:delete"))],
)
async def delete_organization(
    ctx: OrganizationContextDep,
    org_service: Annotated[OrganizationService, Depends(get_organization_service)],
) -> None:
    """Delete an organization."""
    await org_service.delete_organization(ctx.organization.id)


# --- Member APIs ---


@router.post(
    "/{slug}/members",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("organizations:update"))],
)
async def add_member(
    ctx: OrganizationContextDep,
    data: AddMemberRequest,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
):
    """Add a user to the organization."""
    member = await membership_service.add_member(
        org_id=ctx.organization.id,
        user_id=data.user_id,
        role_id=data.role_id,
        invited_by_id=ctx.membership.user_id,
    )
    return {"id": member.id, "user_id": member.user_id, "role_id": member.role_id}


@router.get(
    "/{slug}/members",
)
async def list_members(
    ctx: OrganizationContextDep,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
):
    """List all members of the organization."""
    members = await membership_service.list_members(ctx.organization.id)
    return [
        {
            "id": m.id,
            "user": UserResponse.model_validate(m.user),
            "role": m.role.name,
        }
        for m in members
    ]


@router.patch(
    "/{slug}/members/{member_id}",
    dependencies=[Depends(require_permission("organizations:update"))],
)
async def change_role(
    ctx: OrganizationContextDep,
    member_id: UUID,
    data: ChangeMemberRoleRequest,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
):
    """Change the role of a member."""
    # Note: Currently member_id is the user_id in MembershipService logic
    member = await membership_service.change_role(
        org_id=ctx.organization.id,
        user_id=member_id,
        new_role_id=data.new_role_id,
    )
    return {"id": member.id, "user_id": member.user_id, "role_id": member.role_id}


@router.delete(
    "/{slug}/members/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("organizations:update"))],
)
async def remove_member(
    ctx: OrganizationContextDep,
    member_id: UUID,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
) -> None:
    """Remove a member from the organization."""
    await membership_service.remove_member(
        org_id=ctx.organization.id, user_id=member_id
    )


@router.post(
    "/{slug}/leave",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def leave_organization(
    ctx: OrganizationContextDep,
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
) -> None:
    """Leave the organization. Will fail if the user is the last owner."""
    await membership_service.remove_member(
        org_id=ctx.organization.id, user_id=ctx.membership.user_id
    )
