from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.services.auth_service import AuthService
from app.services.ping_service import PingService
from app.services.user import UserService


def get_ping_service() -> PingService:
    """
    Returns the PingService instance.

    Centralizing dependency creation here makes it easy
    to replace implementations during testing or future
    refactoring.
    """
    return PingService()


async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserService:
    return UserService(db)


async def get_auth_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> AuthService:
    return AuthService(db)
