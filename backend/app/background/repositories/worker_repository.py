from sqlalchemy.ext.asyncio import AsyncSession

from app.background.models.worker import WorkerNode
from app.repositories.base import BaseRepository


class WorkerRepository(BaseRepository[WorkerNode]):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkerNode, db)
