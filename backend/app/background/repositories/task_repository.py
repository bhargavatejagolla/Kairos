from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.background.models.task import BackgroundTask
from app.background.schemas.task import BackgroundTaskCreate

class TaskRepository(BaseRepository[BackgroundTask]):
    def __init__(self, db: AsyncSession):
        super().__init__(BackgroundTask, db)
