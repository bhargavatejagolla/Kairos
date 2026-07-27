from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.api.deps.database import get_db
from app.dependencies.auth import get_current_user
from app.db.models.user import User
from app.notifications.services.notification_service import NotificationService
from app.notifications.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/{id}", response_model=NotificationResponse)
async def get_notification(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NotificationService(db)
    notification = await service.get(id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
