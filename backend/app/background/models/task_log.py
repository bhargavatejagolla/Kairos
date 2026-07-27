from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.models.base import BaseModel

class TaskLog(BaseModel):
    __tablename__ = "task_logs"
    
    task_id = Column(UUID(as_uuid=True), ForeignKey("background_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    level = Column(String, nullable=False, default="INFO")
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    
    task = relationship("BackgroundTask", back_populates="logs")
