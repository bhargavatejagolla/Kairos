from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.core.project import ProjectStatus, ProjectVisibility
from app.schemas.base import SchemaBase
from app.schemas.environment import EnvironmentResponse
from app.schemas.project_settings import ProjectSettingsResponse


class ProjectCreate(SchemaBase):
    name: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=150)
    description: str | None = Field(None, max_length=255)
    environment_id: UUID
    visibility: ProjectVisibility = Field(default=ProjectVisibility.PRIVATE)


class ProjectUpdate(SchemaBase):
    name: str | None = Field(None, max_length=150)
    description: str | None = Field(None, max_length=255)
    environment_id: UUID | None = None
    visibility: ProjectVisibility | None = None
    status: ProjectStatus | None = None


class ProjectResponse(SchemaBase):
    id: UUID
    name: str
    slug: str
    description: str | None
    status: ProjectStatus
    visibility: ProjectVisibility
    environment: EnvironmentResponse
    created_at: datetime
    updated_at: datetime


class ProjectSummary(SchemaBase):
    id: UUID
    name: str
    slug: str
    status: ProjectStatus


class ProjectDetails(ProjectResponse):
    settings: ProjectSettingsResponse | None
