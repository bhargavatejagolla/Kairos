from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.incident import Incident
from app.db.models.organization_member import OrganizationMember
from app.db.models.role import Role


class RecipientResolver:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_incident_recipients(self, incident_id: UUID) -> list[UUID]:
        """Returns the assignee, or if unassigned, all org admins."""
        stmt = select(Incident).where(Incident.id == incident_id)
        result = await self.session.execute(stmt)
        incident = result.scalars().first()
        
        if not incident:
            return []
            
        if incident.assigned_to:
            return [incident.assigned_to]
            
        # Fallback to org admins
        return await self.get_org_admins(incident.organization_id)

    async def get_org_admins(self, organization_id: UUID) -> list[UUID]:
        stmt = select(OrganizationMember.user_id).join(Role).where(
            OrganizationMember.organization_id == organization_id,
            Role.name == "admin"
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_by_id(self, user_id: UUID) -> list[UUID]:
        return [user_id]
