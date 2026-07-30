from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.models.base import BaseModel


class WorkerNode(BaseModel):
    __tablename__ = "worker_nodes"
    
    hostname = Column(String, nullable=False, index=True)
    queue = Column(String, nullable=True)
    version = Column(String, nullable=True)
    cpu = Column(Float, nullable=True)
    memory = Column(Float, nullable=True)
    heartbeat = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="ONLINE")
    running_tasks = Column(Integer, default=0)
