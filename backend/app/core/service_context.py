from dataclasses import dataclass

from app.db.models.environment import Environment
from app.db.models.organization import Organization
from app.db.models.organization_member import OrganizationMember
from app.db.models.project import Project
from app.db.models.project_settings import ProjectSettings
from app.db.models.role import Role
from app.db.models.service import Service


@dataclass
class ServiceContext:
    organization: Organization
    member: OrganizationMember
    role: Role
    project: Project
    environment: Environment
    settings: ProjectSettings
    service: Service
