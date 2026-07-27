from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from app.db.models.enums import AlertSeverity

class EvaluationResult(BaseModel):
    triggered: bool
    rule_id: str
    severity: AlertSeverity
    fingerprint: str
    title: str
    message: str
    metadata_: Optional[Dict[str, Any]] = None
    matched_conditions: List[Dict[str, Any]]
