from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models.organization import Organization
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    def __init__(self, session: Any) -> None:
        super().__init__(Organization, session)

    async def get_by_id(self, org_id: UUID) -> Organization | None:
        """
        Get an organization by ID with members eager loaded.
        """
        stmt = (
            select(Organization)
            .options(selectinload(Organization.members))
            .where(Organization.id == org_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organization | None:
        """
        Get an organization by slug with members eager loaded.
        """
        stmt = (
            select(Organization)
            .options(selectinload(Organization.members))
            .where(Organization.slug == slug)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_slug(self, slug: str) -> bool:
        """
        Check if an organization slug already exists.
        """
        stmt = select(Organization.id).where(Organization.slug == slug).limit(1)
        result = await self.session.execute(stmt)
        return result.first() is not None
