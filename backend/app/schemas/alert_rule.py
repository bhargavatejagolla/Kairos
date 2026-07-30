from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import (
    AggregationType,
    AlertOperator,
    AlertSeverity,
    RuleStatus,
    SignalType,
)


class AlertConditionSchema(BaseModel):
    signal_type: SignalType
    metric_name: str | None = None
    operator: AlertOperator
    threshold: float
    aggregation: AggregationType | None = None
    duration_seconds: int = 300

class RuleCreate(BaseModel):
    name: str
    description: str | None = None
    severity: AlertSeverity
    evaluation_window: str = "5m"
    cooldown: str = "15m"
    conditions: list[AlertConditionSchema]

class RuleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    enabled: bool | None = None
    status: RuleStatus | None = None
    severity: AlertSeverity | None = None
    evaluation_window: str | None = None
    cooldown: str | None = None
    conditions: list[AlertConditionSchema] | None = None

class RuleResponse(BaseModel):
    id: UUID
    service_id: UUID
    name: str
    slug: str
    description: str | None
    enabled: bool
    status: RuleStatus
    severity: AlertSeverity
    evaluation_window: str
    cooldown: str
    model_config = ConfigDict(from_attributes=True)
