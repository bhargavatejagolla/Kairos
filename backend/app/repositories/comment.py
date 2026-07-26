from uuid import UUID
from typing import Sequence
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.db.models.incident_comment import IncidentComment

class CommentRepository(BaseRepository[IncidentComment]):
    def __init__(self, session):
        super().__init__(IncidentComment, session)

    async def list_by_incident(self, incident_id: UUID) -> Sequence[IncidentComment]:
        result = await self.session.execute(
            select(IncidentComment)
            .where(IncidentComment.incident_id == incident_id)
            .order_by(IncidentComment.created_at.asc())
        )
        return result.scalars().all()
