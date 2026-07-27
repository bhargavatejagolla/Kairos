from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Any
from app.api.deps.database import get_db
from app.background.schemas.worker import WorkerResponse
from app.background.repositories.worker_repository import WorkerRepository

router = APIRouter(prefix="/background/workers", tags=["Background Workers"])

@router.get("", response_model=List[WorkerResponse])
async def list_workers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all registered background workers and their status"""
    repo = WorkerRepository(db)
    return await repo.get_multi(skip=skip, limit=limit)
