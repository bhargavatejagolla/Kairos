import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert import Alert
from app.db.models.enums import AlertStatus
from app.repositories.alert import AlertRepository
from app.schemas.evaluation import EvaluationResult
from app.services.correlation_engine import CorrelationEngine
from app.services.maintenance_engine import MaintenanceEngine
from app.services.policy_engine import PolicyEngine
from app.services.silence_engine import SilenceEngine

logger = logging.getLogger(__name__)

class AlertEngine:
    """
    Owns the Alert lifecycle and orchestrates downstream engines.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.alert_repo = AlertRepository(session)
        self.silence_engine = SilenceEngine(session)
        self.maintenance_engine = MaintenanceEngine(session)
        self.correlation_engine = CorrelationEngine(session)
        self.policy_engine = PolicyEngine(session)

    async def process_evaluation(self, organization_id: UUID, project_id: UUID, service_id: UUID, result: EvaluationResult) -> Alert | None:
        if not result.triggered:
            return None
            
        # Check if already exists (Deduplication)
        existing_alert = await self.alert_repo.get_by_fingerprint(result.fingerprint, AlertStatus.OPEN)
        if existing_alert:
            logger.info(f"Alert {result.fingerprint} already OPEN, ignoring.")
            return existing_alert
            
        # Create Alert
        alert = Alert(
            rule_id=UUID(result.rule_id),
            service_id=service_id,
            status=AlertStatus.OPEN,
            severity=result.severity,
            title=result.title,
            message=result.message,
            fingerprint=result.fingerprint,
            triggered_at=datetime.now(timezone.utc)
        )
        self.session.add(alert)
        await self.session.flush() # Needed to get alert.id for correlations
        
        # Check Suppression
        if await self.silence_engine.is_silenced(service_id, alert) or \
           await self.maintenance_engine.is_active(service_id, alert):
            alert.status = AlertStatus.SUPPRESSED
            await self.session.commit()
            return alert
            
        # Correlate
        group = await self.correlation_engine.correlate(organization_id, alert)
        
        # Apply Policy
        await self.policy_engine.apply(organization_id, project_id, alert, group)
        
        await self.session.commit()
        await self.session.refresh(alert)
        
        # Transactional Outbox for Domain Events
        from app.events.outbox_service import OutboxService
        from app.events.schema import DomainEvent
        from app.middleware.correlation import correlation_id_var
        
        outbox = OutboxService(self.session)
        event = DomainEvent(
            event_type="AlertTriggered",
            organization_id=str(organization_id),
            project_id=str(project_id),
            resource_type="ALERT",
            resource_id=str(alert.id),
            actor_id="SYSTEM",
            correlation_id=correlation_id_var.get(None),
            payload={
                "title": alert.title,
                "severity": alert.severity.value,
            }
        )
        await outbox.save_event(event)
        
        # Increment metric
        from app.core.metrics import alerts_triggered_total
        alerts_triggered_total.labels(
            organization_id=str(organization_id),
            source="evaluation_engine"
        ).inc()

        
        return alert

    async def acknowledge(self, alert_id: UUID) -> Alert:
        alert = await self.alert_repo.get(alert_id)
        if alert and alert.status == AlertStatus.OPEN:
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.acknowledged_at = datetime.now(timezone.utc)
            await self.session.commit()
        return alert

    async def resolve(self, alert_id: UUID) -> Alert:
        alert = await self.alert_repo.get(alert_id)
        if alert and alert.status in [AlertStatus.OPEN, AlertStatus.ACKNOWLEDGED]:
            alert.status = AlertStatus.RESOLVED
            alert.resolved_at = datetime.now(timezone.utc)
            await self.session.commit()
        return alert
