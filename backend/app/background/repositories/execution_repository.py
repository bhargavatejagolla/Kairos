from sqlalchemy.ext.asyncio import AsyncSession

from app.background.models.execution import TaskExecution
from app.repositories.base import BaseRepository


class ExecutionRepository(BaseRepository[TaskExecution]):
    def __init__(self, db: AsyncSession):
        super().__init__(TaskExecution, db)
