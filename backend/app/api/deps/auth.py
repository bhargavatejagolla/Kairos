from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.database import get_db
from app.core.exceptions import UnauthorizedException
from app.core.jwt import verify_token
from app.db.models.user import User
from app.repositories.user import UserRepository

reusable_oauth2 = HTTPBearer(auto_error=False)


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[HTTPAuthorizationCredentials | None, Depends(reusable_oauth2)],
) -> User:
    """Extract and verify access token, returning the authenticated User model."""
    if not token:
        raise UnauthorizedException("Not authenticated")

    payload = verify_token(token.credentials, expected_type="access")
    user_id_str = payload.get("sub")
    if not user_id_str:
        raise UnauthorizedException("Invalid token payload")

    try:
        user_id = UUID(str(user_id_str))
    except ValueError:
        raise UnauthorizedException("Invalid user ID in token")

    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)
    if not user:
        raise UnauthorizedException("User not found")

    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(
    current_user: CurrentUserDep,
) -> User:
    """Ensure the authenticated user is currently active."""
    if not current_user.is_active:
        raise UnauthorizedException("Inactive user")
    return current_user


ActiveUserDep = Annotated[User, Depends(get_current_active_user)]
