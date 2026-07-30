from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.notifications.models.template import EmailTemplate
from app.notifications.repositories.template_repository import TemplateRepository
from app.notifications.schemas.template import EmailTemplateCreate, EmailTemplateUpdate


class TemplateService:
    def __init__(self, session: AsyncSession):
        self.repository = TemplateRepository(session)

    async def get_by_slug(self, slug: str, organization_id: UUID | None = None) -> EmailTemplate | None:
        return await self.repository.get_by_slug(slug, organization_id)

    async def create(self, template_in: EmailTemplateCreate) -> EmailTemplate:
        template = await self.repository.create(template_in.model_dump())
        return template

    async def update(self, id: UUID, template_in: EmailTemplateUpdate) -> EmailTemplate:
        template = await self.repository.update(id, template_in.model_dump(exclude_unset=True))
        return template
