from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.notifications.schemas.preference import (
    NotificationPreferenceResponse,
    NotificationPreferenceUpdate,
)
from app.notifications.services.preference_service import PreferenceService

router = APIRouter(prefix="/preferences", tags=["Notification Preferences"])

@router.get("/me", response_model=NotificationPreferenceResponse)
async def get_my_preferences(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = PreferenceService(db)
    return await service.get_or_create(current_user.id)

@router.patch("/me", response_model=NotificationPreferenceResponse)
async def update_my_preferences(
    preference_in: NotificationPreferenceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = PreferenceService(db)
    return await service.update(current_user.id, preference_in)
