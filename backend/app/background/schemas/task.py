from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.background.enums.task_category import TaskCategory
from app.background.enums.task_priority import TaskPriority
from app.background.enums.task_state import TaskState


class BackgroundTaskBase(BaseModel):
    task_name: str
    queue: str
    category: TaskCategory
    priority: TaskPriority = TaskPriority.NORMAL

class BackgroundTaskCreate(BackgroundTaskBase):
    organization_id: UUID | None = None
    project_id: UUID | None = None
    created_by: UUID | None = None
    request_id: str | None = None

class BackgroundTaskResponse(BackgroundTaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    status: TaskState
    progress: float
    current_step: int
    total_steps: int
    retry_count: int
    worker: str | None
    started_at: datetime | None
    completed_at: datetime | None
    duration: float | None
    result: Any | None
