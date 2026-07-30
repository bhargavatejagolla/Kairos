from sqlalchemy.ext.asyncio import AsyncSession

from app.background.models.task import BackgroundTask
from app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[BackgroundTask]):
    def __init__(self, db: AsyncSession):
        super().__init__(BackgroundTask, db)
