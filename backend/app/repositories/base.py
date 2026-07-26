from __future__ import annotations

from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """Generic repository providing reusable CRUD operations."""

    def __init__(
        self,
        model: type[ModelType],
        session: AsyncSession,
    ) -> None:
        self.model = model
        self.session = session

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(
        self,
        obj_id: UUID,
    ) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def list(self) -> list[ModelType]:
        """Alias for get_all."""
        return await self.get_all()

    async def exists(self, obj_id: UUID) -> bool:
        return (await self.get_by_id(obj_id)) is not None

    async def delete(
        self,
        obj_id: UUID,
    ) -> bool:
        result = await self.session.execute(
            delete(self.model).where(self.model.id == obj_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def count(self) -> int:
        result = await self.session.execute(
            select(func.count()).select_from(self.model)
        )
        return int(result.scalar_one())
