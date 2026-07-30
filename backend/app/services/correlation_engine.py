import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.db.models.alert_correlation import AlertCorrelation
from app.db.models.alert_group import AlertGroup
from app.repositories.alert_group import AlertGroupRepository

logger = logging.getLogger(__name__)

class CorrelationEngine:
    """
    Reduces alert storms by correlating alerts into AlertGroups based on ServiceDependencies and time windows.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.group_repo = AlertGroupRepository(session)

    async def correlate(self, organization_id: UUID, alert: Alert, correlation_window_seconds: int = 900) -> AlertGroup:
        """
        Finds an existing active AlertGroup for this alert, or creates a new one.
        """
        # A simple correlation key for now (in production, we'd traverse the ServiceDependency graph)
        correlation_key = f"svc_{alert.service_id}_time_{alert.triggered_at.strftime('%Y%m%d%H')}"
        
        group = await self.group_repo.get_by_correlation_key(organization_id, correlation_key, status="OPEN")
        
        if not group:
            group = AlertGroup(
                organization_id=organization_id,
                root_alert_id=alert.id,
                correlation_key=correlation_key,
                status="OPEN",
                summary=f"Group for {alert.title}",
                opened_at=alert.triggered_at
            )
            self.session.add(group)
            await self.session.flush()
            
        correlation = AlertCorrelation(
            alert_id=alert.id,
            group_id=group.id,
            reason="Temporal and Service correlation",
            score=0.9
        )
        self.session.add(correlation)
        
        return group
