from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AICache(Base):
    __tablename__ = "ai_cache"

    prompt_hash: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    provider: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(255))
    response: Mapped[str] = mapped_column(Text)
    
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
