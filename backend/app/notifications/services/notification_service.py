from uuid import UUID
from datetime import datetime
from app.notifications.repositories.notification_repository import NotificationRepository
from app.notifications.repositories.delivery_audit_repository import AuditRepository, DeliveryRepository
from app.notifications.models.notification import Notification
from app.notifications.schemas.notification import NotificationCreate
from app.notifications.enums.status import NotificationStatus
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

logger = structlog.get_logger(__name__)

class NotificationService:
    def __init__(self, session: AsyncSession):
        self.repository = NotificationRepository(session)
        self.audit_repository = AuditRepository(session)
        self.delivery_repository = DeliveryRepository(session)

    async def create(self, notification_in: NotificationCreate) -> Notification:
        notification = await self.repository.create(notification_in.model_dump())
        await self.audit(notification.id, "Created", "system")
        return notification

    async def get(self, id: UUID) -> Notification | None:
        return await self.repository.get_by_id(id)

    async def update_status(self, id: UUID, status: NotificationStatus) -> Notification:
        update_data = {"status": status}
        if status == NotificationStatus.SENT:
            update_data["sent_at"] = datetime.utcnow()
        elif status == NotificationStatus.FAILED:
            update_data["failed_at"] = datetime.utcnow()
            
        notification = await self.repository.update(id, update_data)
        await self.audit(id, f"Status changed to {status.value}", "system")
        return notification

    async def audit(self, notification_id: UUID, action: str, performed_by: str, metadata: dict = None):
        await self.audit_repository.create({
            "notification_id": notification_id,
            "action": action,
            "performed_by": performed_by,
            "metadata_info": metadata
        })

    async def record_delivery_attempt(
        self, 
        notification_id: UUID, 
        provider: str, 
        status: str, 
        duration_ms: int,
        error_message: str | None = None
    ):
        await self.delivery_repository.create({
            "notification_id": notification_id,
            "provider": provider,
            "status": status,
            "started_at": datetime.utcnow(), # Approximate for now
            "completed_at": datetime.utcnow(),
            "duration_ms": duration_ms,
            "error_message": error_message
        })
