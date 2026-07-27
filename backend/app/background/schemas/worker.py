from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class WorkerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    hostname: str
    queue: Optional[str]
    status: str
    running_tasks: int
    heartbeat: Optional[datetime]
