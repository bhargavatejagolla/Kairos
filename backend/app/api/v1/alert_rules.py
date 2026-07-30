
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.alert import get_alert_context
from app.api.deps.database import get_db
from app.db.models.alert_condition import AlertCondition
from app.db.models.alert_rule import AlertRule
from app.db.models.rule_definition import RuleDefinition
from app.repositories.alert_rule import AlertRuleRepository
from app.schemas.alert_rule import RuleCreate, RuleResponse
from app.workflow.workflow_context import AlertContext

router = APIRouter(prefix="/services/{service_id}/rules", tags=["Alert Rules"])

@router.post("", response_model=RuleResponse, status_code=status.HTTP_201_CREATED)
async def create_rule(
    rule_data: RuleCreate,
    db: AsyncSession = Depends(get_db),
    ctx: AlertContext = Depends(get_alert_context),
):
    """
    Create a new alert rule and its first versioned definition.
    """
    repo = AlertRuleRepository(db)
    
    rule = AlertRule(
        service_id=ctx.service.id,
        name=rule_data.name,
        slug=rule_data.name.lower().replace(" ", "-"),
        description=rule_data.description,
        severity=rule_data.severity,
        evaluation_window=rule_data.evaluation_window,
        cooldown=rule_data.cooldown
    )
    db.add(rule)
    await db.flush()
    
    # Create version 1 definition
    definition = RuleDefinition(
        rule_id=rule.id,
        version=1,
        conditions_payload=[c.model_dump() for c in rule_data.conditions]
    )
    db.add(definition)
    await db.flush()
    
    # Create condition entities
    for condition_data in rule_data.conditions:
        condition = AlertCondition(
            definition_id=definition.id,
            signal_type=condition_data.signal_type,
            metric_name=condition_data.metric_name,
            operator=condition_data.operator,
            threshold=condition_data.threshold,
            aggregation=condition_data.aggregation,
            duration_seconds=condition_data.duration_seconds
        )
        db.add(condition)
        
    await db.commit()
    await db.refresh(rule)
    return rule
