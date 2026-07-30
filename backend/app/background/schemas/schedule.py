from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    task_name: str
    cron: str
    enabled: bool
    next_run: datetime | None
    last_run: datetime | None
