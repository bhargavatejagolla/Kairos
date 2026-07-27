from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.background.models.worker import WorkerNode

class WorkerRepository(BaseRepository[WorkerNode]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkerNode, db)
