from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.models.base import BaseModel
from app.background.enums.task_state import TaskState

class TaskExecution(BaseModel):
    __tablename__ = "task_executions"
    
    task_id = Column(UUID(as_uuid=True), ForeignKey("background_tasks.id", ondelete="CASCADE"), nullable=False, index=True)
    attempt = Column(Integer, nullable=False)
    worker = Column(String, nullable=True)
    status = Column(SQLEnum(TaskState), nullable=False)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Float, nullable=True)
    
    exception = Column(Text, nullable=True)
    traceback = Column(Text, nullable=True)
    
    task = relationship("BackgroundTask", back_populates="executions")
