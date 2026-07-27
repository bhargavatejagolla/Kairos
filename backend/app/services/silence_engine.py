import logging
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.alert import Alert
from app.repositories.silence import SilenceRepository

logger = logging.getLogger(__name__)

class SilenceEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.silence_repo = SilenceRepository(session)

    async def is_silenced(self, service_id: UUID, alert: Alert) -> bool:
        """
        Checks if the given alert is suppressed by an active silence.
        """
        current_time = datetime.now(timezone.utc)
        active_silences = await self.silence_repo.get_active_silences(service_id, current_time)
        
        for silence in active_silences:
            # Here we would do a more complex matcher on alert metadata/labels
            # For now, if there is a silence for the service, we silence it.
            return True
            
        return False
