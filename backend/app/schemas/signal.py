from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.db.models.enums import AlertSource, SignalType


class SignalIn(BaseModel):
    signal_type: SignalType
    source: AlertSource
    value: float | None = None
    unit: str | None = None
    metadata_: dict[str, Any] | None = None
    received_at: datetime

class SignalOut(SignalIn):
    id: UUID
    service_id: UUID
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
