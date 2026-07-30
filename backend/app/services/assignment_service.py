from uuid import UUID

from app.core.exceptions import BadRequestException
from app.db.models.incident import Incident
from app.repositories.incident import IncidentRepository
from app.repositories.user import UserRepository


class AssignmentService:
    def __init__(self, incident_repo: IncidentRepository, user_repo: UserRepository):
        self.incident_repo = incident_repo
        self.user_repo = user_repo

    async def assign_incident(self, incident: Incident, user_id: UUID) -> Incident:
        user = await self.user_repo.get(user_id)
        if not user:
            raise BadRequestException(f"User {user_id} does not exist.")
            
        incident.assigned_to = user_id
        await self.incident_repo.update(incident)
        return incident
        
    async def unassign_incident(self, incident: Incident) -> Incident:
        incident.assigned_to = None
        await self.incident_repo.update(incident)
        return incident
