from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import TimelineEvent


class TimelineEntryCreate(BaseModel):
    event_type: TimelineEvent
    message: str | None = None
    metadata_: dict[str, Any] = {}

class TimelineEntryResponse(TimelineEntryCreate):
    id: UUID
    incident_id: UUID
    actor_id: UUID | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
