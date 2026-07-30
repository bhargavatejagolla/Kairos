from typing import Any

from pydantic import BaseModel

from app.db.models.enums import AlertSeverity


class EvaluationResult(BaseModel):
    triggered: bool
    rule_id: str
    severity: AlertSeverity
    fingerprint: str
    title: str
    message: str
    metadata_: dict[str, Any] | None = None
    matched_conditions: list[dict[str, Any]]
