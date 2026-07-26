from uuid import UUID
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.incident_timeline import IncidentTimeline
from app.db.models.enums import TimelineEvent
from app.repositories.timeline import TimelineRepository
from app.schemas.timeline import TimelineEntryCreate

class TimelineService:
    def __init__(self, repository: TimelineRepository):
        self.repository = repository

    async def add_entry(
        self,
        incident_id: UUID,
        event_type: TimelineEvent,
        actor_id: UUID | None = None,
        message: str | None = None,
        metadata: dict = None
    ) -> IncidentTimeline:
        if not metadata:
            metadata = {}
            
        entry = IncidentTimeline(
            incident_id=incident_id,
            event_type=event_type,
            actor_id=actor_id,
            message=message,
            metadata_=metadata,
            created_at=datetime.now(UTC)
        )
        
        await self.repository.add(entry)
        return entry
        
    async def list_by_incident(self, incident_id: UUID) -> list[IncidentTimeline]:
        return await self.repository.list_by_incident(incident_id)
