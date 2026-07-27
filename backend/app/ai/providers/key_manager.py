from datetime import datetime, timezone
import logging
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.api_key import APIKey

logger = logging.getLogger(__name__)

class KeyManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_available_key(self, provider: str) -> APIKey | None:
        # Get highest priority active key not in cooldown
        now = datetime.now(timezone.utc)
        stmt = (
            select(APIKey)
            .where(APIKey.provider == provider)
            .where(APIKey.enabled == True)
            .where(APIKey.status == "active")
            .where((APIKey.cooldown_until == None) | (APIKey.cooldown_until < now))
            .order_by(APIKey.priority.desc(), APIKey.last_used.asc().nullsfirst())
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    async def record_usage(self, key_id: UUID, tokens: int):
        stmt = select(APIKey).where(APIKey.id == key_id)
        result = await self.db.execute(stmt)
        key = result.scalar_one_or_none()
        if key:
            key.tokens_today += tokens
            key.requests_today += 1
            key.last_used = datetime.now(timezone.utc)
            await self.db.commit()
            
    async def record_failure(self, key_id: UUID, cooldown_seconds: int = 60):
        stmt = select(APIKey).where(APIKey.id == key_id)
        result = await self.db.execute(stmt)
        key = result.scalar_one_or_none()
        if key:
            key.failure_count += 1
            key.status = "rate_limited"
            key.cooldown_until = datetime.now(timezone.utc)
            # Add seconds to cooldown_until (not fully implemented here, conceptual)
            await self.db.commit()
