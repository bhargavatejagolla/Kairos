from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hostname: str
    queue: str | None
    status: str
    running_tasks: int
    heartbeat: datetime | None
