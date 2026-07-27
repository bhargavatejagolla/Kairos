from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.db.models.enums import RuleStatus, AlertSeverity, SignalType, AlertOperator, AggregationType

class AlertConditionSchema(BaseModel):
    signal_type: SignalType
    metric_name: Optional[str] = None
    operator: AlertOperator
    threshold: float
    aggregation: Optional[AggregationType] = None
    duration_seconds: int = 300

class RuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    severity: AlertSeverity
    evaluation_window: str = "5m"
    cooldown: str = "15m"
    conditions: List[AlertConditionSchema]

class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    status: Optional[RuleStatus] = None
    severity: Optional[AlertSeverity] = None
    evaluation_window: Optional[str] = None
    cooldown: Optional[str] = None
    conditions: Optional[List[AlertConditionSchema]] = None

class RuleResponse(BaseModel):
    id: UUID
    service_id: UUID
    name: str
    slug: str
    description: Optional[str]
    enabled: bool
    status: RuleStatus
    severity: AlertSeverity
    evaluation_window: str
    cooldown: str
    model_config = ConfigDict(from_attributes=True)
