from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict
from app.background.enums.task_state import TaskState
from app.background.enums.task_priority import TaskPriority
from app.background.enums.task_category import TaskCategory

class BackgroundTaskBase(BaseModel):
    task_name: str
    queue: str
    category: TaskCategory
    priority: TaskPriority = TaskPriority.NORMAL

class BackgroundTaskCreate(BackgroundTaskBase):
    organization_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    request_id: Optional[str] = None

class BackgroundTaskResponse(BackgroundTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: TaskState
    progress: float
    current_step: int
    total_steps: int
    retry_count: int
    worker: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    duration: Optional[float]
    result: Optional[Any]
