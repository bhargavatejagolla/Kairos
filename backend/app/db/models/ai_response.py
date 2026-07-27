import uuid
from sqlalchemy import String, ForeignKey, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import BaseModel

class AIResponse(BaseModel):
    __tablename__ = "ai_responses"

    conversation_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("ai_conversations.id", ondelete="SET NULL"), nullable=True, index=True)
    incident_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True, index=True)
    alert_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("alerts.id", ondelete="SET NULL"), nullable=True, index=True)
    
    provider: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(255))
    prompt_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    response: Mapped[str] = mapped_column(Text)
    
    latency: Mapped[float | None] = mapped_column(Float, nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
