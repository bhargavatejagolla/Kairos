import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.workflow.workflow_context import AlertContext
from app.schemas.signal import SignalIn
from app.db.models.signal import Signal
from app.db.models.alert import Alert

from app.services.signal_service import SignalService
from app.services.rule_engine import RuleEngine
from app.repositories.alert_rule import AlertRuleRepository
from app.services.alert_engine import AlertEngine

logger = logging.getLogger(__name__)

class AlertWorkflow:
    """
    The master orchestrator for the Alert Management Domain.
    Ties together Signals -> Rule Engine -> Correlation -> Alert Engine -> Incident Workflow.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.signal_service = SignalService(session)
        self.rule_engine = RuleEngine()
        self.rule_repo = AlertRuleRepository(session)
        self.alert_engine = AlertEngine(session)

    async def ingest_signal(self, ctx: AlertContext, signal_data: SignalIn) -> Signal:
        """
        Main entrypoint for telemetry ingestion.
        """
        logger.info(f"event=signal_received service={ctx.service.id} type={signal_data.signal_type}")
        
        # 1. Store Immutable Signal
        signal = await self.signal_service.ingest(ctx.service.id, signal_data)
        
        # 2. Load Active Rules
        active_rules = await self.rule_repo.get_active_rules()
        service_rules = [r for r in active_rules if r.service_id == ctx.service.id]
        
        if not service_rules:
            return signal
            
        # 3. Pure Evaluation
        evaluations = self.rule_engine.evaluate(signal, service_rules)
        
        # 4. Process Alerts for any triggered evaluations
        for eval_result in evaluations:
            await self.alert_engine.process_evaluation(
                organization_id=ctx.organization.id,
                project_id=ctx.project.id,
                service_id=ctx.service.id,
                result=eval_result
            )
            
        return signal

    async def acknowledge_alert(self, ctx: AlertContext, alert_id: UUID) -> Alert:
        logger.info(f"event=alert_acknowledge alert_id={alert_id} user={ctx.actor.id}")
        return await self.alert_engine.acknowledge(alert_id)

    async def resolve_alert(self, ctx: AlertContext, alert_id: UUID) -> Alert:
        logger.info(f"event=alert_resolve alert_id={alert_id} user={ctx.actor.id}")
        return await self.alert_engine.resolve(alert_id)
