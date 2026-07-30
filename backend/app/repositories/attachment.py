from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.db.models.incident_attachment import IncidentAttachment
from app.repositories.base import BaseRepository


class AttachmentRepository(BaseRepository[IncidentAttachment]):
    def __init__(self, session):
        super().__init__(IncidentAttachment, session)

    async def list_by_incident(self, incident_id: UUID) -> Sequence[IncidentAttachment]:
        result = await self.session.execute(
            select(IncidentAttachment)
            .where(IncidentAttachment.incident_id == incident_id)
            .order_by(IncidentAttachment.created_at.desc())
        )
        return result.scalars().all()
