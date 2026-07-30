from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.db.models.user import User
from app.dependencies.auth import get_current_user
from app.notifications.schemas.template import (
    EmailTemplateCreate,
    EmailTemplateResponse,
    EmailTemplateUpdate,
)
from app.notifications.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["Notification Templates"])

@router.post("", response_model=EmailTemplateResponse)
async def create_template(
    template_in: EmailTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TemplateService(db)
    return await service.create(template_in)

@router.patch("/{id}", response_model=EmailTemplateResponse)
async def update_template(
    id: UUID,
    template_in: EmailTemplateUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TemplateService(db)
    return await service.update(id, template_in)
