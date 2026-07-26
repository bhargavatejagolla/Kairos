from typing import Any
from uuid import UUID

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from app.db.models.organization_member import OrganizationMember
from app.repositories.base import BaseRepository


class OrganizationMemberRepository(BaseRepository[OrganizationMember]):
    def __init__(self, session: Any) -> None:
        super().__init__(OrganizationMember, session)

    async def get_member(
        self, org_id: UUID, user_id: UUID
    ) -> OrganizationMember | None:
        """
        Get a specific organization member by org_id and user_id.
        """
        stmt = (
            select(OrganizationMember)
            .options(selectinload(OrganizationMember.role))
            .where(
                and_(
                    OrganizationMember.organization_id == org_id,
                    OrganizationMember.user_id == user_id,
                )
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_members(self, org_id: UUID) -> list[OrganizationMember]:
        """
        List all members of an organization.
        """
        stmt = (
            select(OrganizationMember)
            .options(
                selectinload(OrganizationMember.role),
                selectinload(OrganizationMember.user),
            )
            .where(OrganizationMember.organization_id == org_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def list_user_organizations(self, user_id: UUID) -> list[OrganizationMember]:
        """
        List all organizations a user belongs to.
        """
        stmt = (
            select(OrganizationMember)
            .options(
                selectinload(OrganizationMember.organization),
                selectinload(OrganizationMember.role),
            )
            .where(OrganizationMember.user_id == user_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def is_member(self, org_id: UUID, user_id: UUID) -> bool:
        """
        Check if a user is a member of an organization.
        """
        stmt = (
            select(OrganizationMember.id)
            .where(
                and_(
                    OrganizationMember.organization_id == org_id,
                    OrganizationMember.user_id == user_id,
                )
            )
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.first() is not None

    async def change_role(self, org_id: UUID, user_id: UUID, new_role_id: UUID) -> OrganizationMember | None:
        """
        Change a member's role.
        """
        member = await self.get_member(org_id, user_id)
        if member:
            member.role_id = new_role_id
            await self.session.flush()
        return member

    async def remove_member(self, org_id: UUID, user_id: UUID) -> None:
        """
        Remove a member from an organization.
        """
        member = await self.get_member(org_id, user_id)
        if member:
            await self.delete(member.id)
            
    async def add_member(self, member: OrganizationMember) -> OrganizationMember:
        """
        Add a new member to an organization.
        """
        return await self.create(member)
