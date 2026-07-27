from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_name: str
    cron: str
    enabled: bool
    next_run: Optional[datetime]
    last_run: Optional[datetime]
