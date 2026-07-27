from sqlalchemy import Column, String, Boolean, DateTime
from app.db.models.base import BaseModel

class TaskSchedule(BaseModel):
    __tablename__ = "task_schedules"
    
    task_name = Column(String, nullable=False, index=True)
    cron = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    next_run = Column(DateTime(timezone=True), nullable=True)
    last_run = Column(DateTime(timezone=True), nullable=True)
