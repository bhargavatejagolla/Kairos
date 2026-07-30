from collections.abc import Sequence
from uuid import UUID

from app.core.exceptions import DuplicateResourceException as ResourceAlreadyExistsError
from app.core.exceptions import ResourceNotFoundException as ResourceNotFoundError
from app.core.project_context import ProjectContext
from app.db.models.service import Service
from app.repositories.service import ServiceRepository
from app.schemas.service import ServiceCreate, ServiceUpdate


class ServiceService:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository

    async def get_by_id(self, service_id: UUID) -> Service:
        service = await self.repository.get_with_details(service_id)
        if not service:
            raise ResourceNotFoundError(f"Service {service_id} not found")
        return service

    async def list_by_project(self, context: ProjectContext, skip: int = 0, limit: int = 100) -> Sequence[Service]:
        return await self.repository.list_by_project(context.project_id, skip=skip, limit=limit)

    async def create(self, context: ProjectContext, data: ServiceCreate, created_by: UUID | None = None) -> Service:
        existing = await self.repository.get_by_slug(context.organization_id, context.project_id, data.slug)
        if existing:
            raise ResourceAlreadyExistsError(f"Service with slug '{data.slug}' already exists in this project")

        service = Service(
            organization_id=context.organization_id,
            project_id=context.project_id,
            environment_id=context.environment_id,
            created_by_id=created_by,
            **data.model_dump()
        )
        await self.repository.add(service)
        return service

    async def update(self, service: Service, data: ServiceUpdate, updated_by: UUID | None = None) -> Service:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(service, field, value)
            
        service.updated_by_id = updated_by
        return await self.repository.update(service)

    async def delete(self, service: Service) -> None:
        await self.repository.delete(service)
