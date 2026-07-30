from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.models.incident_comment import IncidentComment
from app.repositories.base import BaseRepository


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
