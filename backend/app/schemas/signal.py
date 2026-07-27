from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.db.models.enums import SignalType, AlertSource

class SignalIn(BaseModel):
    signal_type: SignalType
    source: AlertSource
    value: Optional[float] = None
    unit: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = None
    received_at: datetime

class SignalOut(SignalIn):
    id: UUID
    service_id: UUID
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
