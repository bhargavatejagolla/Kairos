from datetime import datetime, timezone
from uuid import uuid4

from app.db.models.alert_condition import AlertCondition
from app.db.models.alert_rule import AlertRule
from app.db.models.enums import AlertOperator, SignalType
from app.db.models.rule_definition import RuleDefinition
from app.db.models.signal import Signal
from app.services.rule_engine import RuleEngine


def test_rule_engine_evaluation():
    engine = RuleEngine()
    
    # 1. Setup mock signal
    signal = Signal(
        service_id=uuid4(),
        signal_type=SignalType.METRIC,
        value=95.0,
        received_at=datetime.now(timezone.utc)
    )
    
    # 2. Setup mock rule
    condition = AlertCondition(
        signal_type=SignalType.METRIC,
        operator=AlertOperator.GREATER_THAN,
        threshold=90.0,
        duration_seconds=300
    )
    definition = RuleDefinition(
        version=1,
        conditions=[condition]
    )
    from app.db.models.enums import AlertSeverity
    rule = AlertRule(
        id=uuid4(),
        service_id=signal.service_id,
        name="High CPU",
        severity=AlertSeverity.CRITICAL,
        definitions=[definition]
    )
    
    # 3. Evaluate
    results = engine.evaluate(signal, [rule])
    
    # 4. Assert
    assert len(results) == 1
    assert results[0].triggered is True
    assert results[0].rule_id == str(rule.id)
