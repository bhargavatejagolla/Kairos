from pydantic import BaseModel
from typing import Dict

class IncidentStatistics(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    by_severity: Dict[str, int]
    by_status: Dict[str, int]
    mttr_minutes: float | None = None # Mean time to resolution
    mtta_minutes: float | None = None # Mean time to acknowledge
