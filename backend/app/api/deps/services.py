from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.services.auth_service import AuthService
from app.services.authorization import AuthorizationService
from app.services.membership_service import MembershipService
from app.services.organization_service import OrganizationService
from app.services.ping_service import PingService
from app.services.role_service import RoleService
from app.services.user import UserService


def get_ping_service() -> PingService:
    """
    Returns the PingService instance.

    Centralizing dependency creation here makes it easy
    to replace implementations during testing or future
    refactoring.
    """
    return PingService()


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserService:
    return UserService(db)


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    return AuthService(db)


async def get_role_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RoleService:
    from app.repositories.permission import PermissionRepository
    from app.repositories.role import RoleRepository
    from app.services.role_service import RoleService

    return RoleService(
        role_repository=RoleRepository(db),
        permission_repository=PermissionRepository(db),
    )


def get_authorization_service() -> AuthorizationService:
    from app.services.authorization import AuthorizationService

    return AuthorizationService()


async def get_membership_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MembershipService:
    from app.repositories.organization_member import OrganizationMemberRepository
    from app.repositories.role import RoleRepository
    from app.services.membership_service import MembershipService

    return MembershipService(
        membership_repo=OrganizationMemberRepository(db),
        role_repo=RoleRepository(db),
    )


async def get_organization_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    membership_service: Annotated[MembershipService, Depends(get_membership_service)],
) -> OrganizationService:
    from app.repositories.organization import OrganizationRepository
    from app.services.organization_service import OrganizationService

    return OrganizationService(
        org_repo=OrganizationRepository(db),
        membership_service=membership_service,
    )
