from uuid import UUID
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as aioredis

from app.core.config import settings
from app.notifications.services.preference_service import PreferenceService

logger = structlog.get_logger(__name__)

class PolicyEngine:
    def __init__(self, session: AsyncSession):
        self.preference_service = PreferenceService(session)
        self.redis = aioredis.from_url(settings.redis_url)
        self.suppression_window_seconds = 60 * 5 # 5 minutes default

    async def evaluate(self, user_id: UUID, category: str, deduplication_key: str | None = None) -> bool:
        """
        Returns True if the notification should be sent.
        Returns False if suppressed by preferences or rate limits.
        """
        # 1. Check User Preferences
        is_enabled = await self.preference_service.is_enabled(user_id, category)
        if not is_enabled:
            logger.info("notification_suppressed_by_preference", user_id=str(user_id), category=category)
            return False

        # 2. Check Suppression Engine (Redis Deduplication)
        if deduplication_key:
            # We construct a unique key for this exact event + user combination
            redis_key = f"kairos:notify:suppress:{user_id}:{deduplication_key}"
            
            # Use SETNX to set the key if it doesn't exist
            # If it already exists, SETNX returns 0 (suppress this notification)
            is_new = await self.redis.set(redis_key, "1", ex=self.suppression_window_seconds, nx=True)
            if not is_new:
                logger.info("notification_suppressed_by_engine", redis_key=redis_key)
                return False

        return True
