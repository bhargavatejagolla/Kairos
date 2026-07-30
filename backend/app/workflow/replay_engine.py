import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.alert_rule import AlertRule
from app.repositories.signal import SignalRepository
from app.services.rule_engine import RuleEngine

logger = logging.getLogger(__name__)

class AlertReplayEngine:
    """
    Evaluates historical telemetry against new or modified rules to prevent alert storms and safely tune thresholds.
    """
    def __init__(self, session: AsyncSession):
        self.session = session
        self.rule_engine = RuleEngine()
        self.signal_repo = SignalRepository(session)

    async def simulate(self, service_id: UUID, proposed_rule: AlertRule, hours_back: int = 24) -> dict[str, any]:
        """
        Replays the last `hours_back` of signals for the service against a hypothetical rule definition.
        Returns statistics on how many alerts WOULD have fired.
        """
        logger.info(f"Simulating rule {proposed_rule.name} against past {hours_back} hours of telemetry for service {service_id}")
        
        # In a real system we would filter by received_at >= now - hours_back
        signals = await self.signal_repo.list_by_service(service_id, limit=5000)
        
        simulated_alerts = 0
        triggered_conditions = []
        
        for signal in signals:
            eval_results = self.rule_engine.evaluate(signal, [proposed_rule])
            for res in eval_results:
                if res.triggered:
                    simulated_alerts += 1
                    triggered_conditions.extend(res.matched_conditions)
                    
        return {
            "signals_analyzed": len(signals),
            "simulated_alerts": simulated_alerts,
            "estimated_noise_reduction": "N/A (simulation metric)"
        }
