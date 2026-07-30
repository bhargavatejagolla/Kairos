from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.background.enums.task_category import TaskCategory
from app.background.enums.task_priority import TaskPriority
from app.background.enums.task_state import TaskState
from app.db.models.base import BaseModel


class BackgroundTask(BaseModel):
    __tablename__ = "background_tasks"
    
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    task_name = Column(String, nullable=False, index=True)
    queue = Column(String, nullable=False, index=True)
    category = Column(SQLEnum(TaskCategory), nullable=False, index=True)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.NORMAL, nullable=False)
    status = Column(SQLEnum(TaskState), default=TaskState.CREATED, nullable=False, index=True)
    
    progress = Column(Float, default=0.0)
    current_step = Column(Integer, default=0)
    total_steps = Column(Integer, default=1)
    
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    
    worker = Column(String, nullable=True)
    request_id = Column(String, nullable=True, index=True)
    
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Float, nullable=True)
    
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")
