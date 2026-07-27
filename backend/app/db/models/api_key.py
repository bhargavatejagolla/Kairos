from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import BaseModel

class APIKey(BaseModel):
    __tablename__ = "api_keys"

    provider: Mapped[str] = mapped_column(String(100), index=True)
    key_name: Mapped[str] = mapped_column(String(255))
    priority: Mapped[int] = mapped_column(Integer, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(50), default="active") # active, rate_limited, error
    
    last_used: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    requests_today: Mapped[int] = mapped_column(Integer, default=0)
    tokens_today: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    cooldown_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
