from uuid import UUID

from sqlalchemy import and_, select

from app.notifications.models.template import EmailTemplate
from app.repositories.base import BaseRepository


class TemplateRepository(BaseRepository[EmailTemplate]):
    def __init__(self, session):
        super().__init__(EmailTemplate, session)

    async def get_by_slug(self, slug: str, organization_id: UUID | None = None) -> EmailTemplate | None:
        conditions = [EmailTemplate.slug == slug, EmailTemplate.is_active == True]
        if organization_id:
            # Check for org-specific template, fallback to global
            stmt = select(EmailTemplate).where(
                and_(
                    *conditions,
                    EmailTemplate.organization_id == organization_id
                )
            )
            result = await self.session.execute(stmt)
            template = result.scalars().first()
            if template:
                return template
                
        # Global fallback
        stmt = select(EmailTemplate).where(
            and_(
                *conditions,
                EmailTemplate.organization_id == None
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
