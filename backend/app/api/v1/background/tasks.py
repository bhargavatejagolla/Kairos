from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.background.schemas.task import BackgroundTaskCreate, BackgroundTaskResponse
from app.background.services.task_service import TaskService

router = APIRouter(prefix="/background/tasks", tags=["Background Tasks"])

@router.post("", response_model=BackgroundTaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: BackgroundTaskCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new background task manually (Admin)"""
    service = TaskService(db)
    return await service.create_task(task_in)

@router.get("", response_model=list[BackgroundTaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """List all background tasks"""
    service = TaskService(db)
    return await service.repository.get_multi(skip=skip, limit=limit)

@router.get("/{task_id}", response_model=BackgroundTaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific task by ID"""
    service = TaskService(db)
    task = await service.repository.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/{task_id}/retry", response_model=BackgroundTaskResponse)
async def retry_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Retry a failed background task"""
    service = TaskService(db)
    task = await service.repository.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Stub logic for retry
    return task

@router.post("/{task_id}/cancel", response_model=BackgroundTaskResponse)
async def cancel_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Cancel a running or queued background task"""
    service = TaskService(db)
    task = await service.repository.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # Stub logic for cancel
    return task
