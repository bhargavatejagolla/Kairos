import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.repositories.maintenance_window import MaintenanceWindowRepository

logger = logging.getLogger(__name__)

class MaintenanceEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.maintenance_repo = MaintenanceWindowRepository(session)

    async def is_active(self, service_id: UUID, alert: Alert) -> bool:
        """
        Checks if the given alert is suppressed by an active maintenance window.
        """
        current_time = datetime.now(timezone.utc)
        active_windows = await self.maintenance_repo.get_active_windows(service_id, current_time)
        
        if active_windows:
            return True
            
        return False
