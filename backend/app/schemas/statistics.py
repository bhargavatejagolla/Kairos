
from pydantic import BaseModel


class IncidentStatistics(BaseModel):
    total_incidents: int
    open_incidents: int
    resolved_incidents: int
    by_severity: dict[str, int]
    by_status: dict[str, int]
    mttr_minutes: float | None = None # Mean time to resolution
    mtta_minutes: float | None = None # Mean time to acknowledge
