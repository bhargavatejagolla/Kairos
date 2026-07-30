from app.notifications.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session):
        super().__init__(Notification, session)

    async def get_by_status(self, status: str, limit: int = 100):
        # Additional custom queries can be added here
        pass
