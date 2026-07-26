import uuid
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class TokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(RefreshToken, session)

    async def get_by_jti(self, token_id: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_id == token_id)
        )
        return result.scalar_one_or_none()

    async def create_token(
        self, user_id: uuid.UUID, token_id: str, expires_at: datetime
    ) -> RefreshToken:
        token = RefreshToken(
            user_id=user_id,
            token_id=token_id,
            expires_at=expires_at,
            revoked=False,
        )
        return await self.create(token)

    async def revoke_by_jti(self, token_id: str) -> bool:
        token = await self.get_by_jti(token_id)
        if not token or token.revoked:
            return False
        token.revoked = True
        await self.update(token)
        return True

    async def revoke_all_for_user(self, user_id: uuid.UUID) -> int:
        result = await self.session.execute(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
            )
            .values(revoked=True)
        )
        await self.session.commit()
        return result.rowcount
