from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import BaseModel


class AIPrompt(BaseModel):
    __tablename__ = "ai_prompts"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    version: Mapped[int] = mapped_column(default=1)
    system_prompt: Mapped[str] = mapped_column(Text)
    user_template: Mapped[str] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
