from uuid import UUID
from app.repositories.base import BaseRepository
from app.notifications.models.delivery import NotificationDelivery
from app.notifications.models.audit import NotificationAudit

class DeliveryRepository(BaseRepository[NotificationDelivery]):
    def __init__(self, session):
        super().__init__(NotificationDelivery, session)


class AuditRepository(BaseRepository[NotificationAudit]):
    def __init__(self, session):
        super().__init__(NotificationAudit, session)
