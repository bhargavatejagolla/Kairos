from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.models.base import BaseModel

class DeadLetterTask(BaseModel):
    __tablename__ = "dead_letter_tasks"
    
    original_task_id = Column(UUID(as_uuid=True), ForeignKey("background_tasks.id", ondelete="SET NULL"), nullable=True)
    task_name = Column(String, nullable=False)
    queue = Column(String, nullable=False)
    payload = Column(Text, nullable=True)
    
    reason = Column(Text, nullable=False)
    retry_attempts = Column(Integer, default=0)
    failed_at = Column(DateTime(timezone=True), nullable=False)
    
    recovered = Column(Boolean, default=False)
