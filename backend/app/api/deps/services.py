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


async def get_environment_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "EnvironmentService":
    from app.repositories.environment import EnvironmentRepository
    from app.repositories.project import ProjectRepository
    from app.services.environment_service import EnvironmentService

    return EnvironmentService(
        environment_repo=EnvironmentRepository(db),
        project_repo=ProjectRepository(db),
    )


async def get_project_settings_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "ProjectSettingsService":
    from app.repositories.project_settings import ProjectSettingsRepository
    from app.services.project_settings_service import ProjectSettingsService

    return ProjectSettingsService(
        settings_repo=ProjectSettingsRepository(db),
    )


async def get_project_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "ProjectService":
    from app.repositories.environment import EnvironmentRepository
    from app.repositories.project import ProjectRepository
    from app.services.project_service import ProjectService

    return ProjectService(
        project_repo=ProjectRepository(db),
        environment_repo=EnvironmentRepository(db),
        session=db,
    )

async def get_service_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "ServiceService":
    from app.repositories.service import ServiceRepository
    from app.services.service_service import ServiceService

    return ServiceService(
        repository=ServiceRepository(db),
    )

async def get_timeline_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "TimelineService":
    from app.repositories.timeline import TimelineRepository
    from app.services.timeline_service import TimelineService

    return TimelineService(
        repository=TimelineRepository(db),
    )

async def get_workflow_engine() -> "WorkflowEngine":
    from app.core.workflow import WorkflowEngine
    return WorkflowEngine()

async def get_incident_service(
    db: Annotated[AsyncSession, Depends(get_db)],
    timeline_service: Annotated["TimelineService", Depends(get_timeline_service)],
    workflow_engine: Annotated["WorkflowEngine", Depends(get_workflow_engine)],
) -> "IncidentService":
    from app.repositories.incident import IncidentRepository
    from app.services.incident_service import IncidentService

    return IncidentService(
        repository=IncidentRepository(db),
        timeline_service=timeline_service,
        workflow_engine=workflow_engine,
        session=db,
    )

async def get_assignment_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> "AssignmentService":
    from app.repositories.incident import IncidentRepository
    from app.repositories.user import UserRepository
    from app.services.assignment_service import AssignmentService

    return AssignmentService(
        incident_repo=IncidentRepository(db),
        user_repo=UserRepository(db),
    )
