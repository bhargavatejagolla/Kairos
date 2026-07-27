from sqlalchemy.ext.asyncio import AsyncSession
from app.background.repositories.task_repository import TaskRepository
from app.background.schemas.task import BackgroundTaskCreate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repository = TaskRepository(db)
        
    async def create_task(self, task_in: BackgroundTaskCreate):
        return await self.repository.create(task_in)
