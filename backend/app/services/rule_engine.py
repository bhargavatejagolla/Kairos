import logging

from app.db.models.alert_condition import AlertCondition
from app.db.models.alert_rule import AlertRule
from app.db.models.enums import AlertOperator
from app.db.models.signal import Signal
from app.schemas.evaluation import EvaluationResult
from app.services.fingerprint_engine import FingerprintEngine

logger = logging.getLogger(__name__)

class RuleEngine:
    """
    Pure evaluation engine. Does not write to DB.
    """
    def __init__(self):
        self.fingerprint_engine = FingerprintEngine()

    def evaluate(self, signal: Signal, active_rules: list[AlertRule]) -> list[EvaluationResult]:
        """
        Checks a signal against a list of active rules for its service.
        """
        results = []
        for rule in active_rules:
            if not rule.definitions:
                continue
                
            latest_def = sorted(rule.definitions, key=lambda d: d.version, reverse=True)[0]
            
            matched = []
            triggered = False
            for condition in latest_def.conditions:
                if condition.signal_type != signal.signal_type:
                    continue
                
                if self._evaluate_condition(signal, condition):
                    matched.append(condition)
                    
            if matched:
                triggered = True
                
            if triggered:
                fingerprint = self.fingerprint_engine.generate(
                    service_id=str(signal.service_id),
                    rule_id=str(rule.id)
                )
                
                results.append(EvaluationResult(
                    triggered=True,
                    rule_id=str(rule.id),
                    severity=rule.severity,
                    fingerprint=fingerprint,
                    title=f"Alert: {rule.name}",
                    message=f"Signal {signal.signal_type} breached threshold.",
                    matched_conditions=[{"id": str(c.id), "operator": c.operator, "threshold": c.threshold} for c in matched]
                ))
        return results
        
    def _evaluate_condition(self, signal: Signal, condition: AlertCondition) -> bool:
        if signal.value is None:
            return False
            
        if condition.operator == AlertOperator.GREATER_THAN:
            return signal.value > condition.threshold
        elif condition.operator == AlertOperator.GREATER_THAN_EQUAL:
            return signal.value >= condition.threshold
        elif condition.operator == AlertOperator.LESS_THAN:
            return signal.value < condition.threshold
        elif condition.operator == AlertOperator.LESS_THAN_EQUAL:
            return signal.value <= condition.threshold
        elif condition.operator == AlertOperator.EQUAL:
            return signal.value == condition.threshold
        elif condition.operator == AlertOperator.NOT_EQUAL:
            return signal.value != condition.threshold
        return False
