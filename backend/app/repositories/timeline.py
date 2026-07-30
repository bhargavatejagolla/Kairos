from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.models.incident_timeline import IncidentTimeline
from app.repositories.base import BaseRepository


class TimelineRepository(BaseRepository[IncidentTimeline]):
    def __init__(self, session):
        super().__init__(IncidentTimeline, session)

    async def list_by_incident(self, incident_id: UUID) -> Sequence[IncidentTimeline]:
        result = await self.session.execute(
            select(IncidentTimeline)
            .where(IncidentTimeline.incident_id == incident_id)
            .order_by(IncidentTimeline.created_at.asc())
        )
        return result.scalars().all()
