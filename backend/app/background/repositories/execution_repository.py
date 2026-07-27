from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.background.models.execution import TaskExecution

class ExecutionRepository(BaseRepository[TaskExecution]):
    def __init__(self, db: AsyncSession):
        super().__init__(TaskExecution, db)
