from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidCredentialsError,
    UnauthorizedException,
)
from app.core.jwt import create_access_token, create_refresh_token, verify_token
from app.core.security import verify_password
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:
    """Service layer handling authentication, token issuance, and validation."""

    def __init__(
        self,
        session_or_repo: AsyncSession | UserRepository,
    ) -> None:
        if isinstance(session_or_repo, AsyncSession):
            self.repository = UserRepository(session_or_repo)
        else:
            self.repository = session_or_repo

    async def login(self, login_in: LoginRequest) -> TokenResponse:
        """Authenticate user by email/password and issue JWT token pair."""
        user = await self.repository.get_by_email(login_in.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(login_in.password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise UnauthorizedException("User account is inactive")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Verify refresh token and issue a new JWT token pair."""
        payload = verify_token(refresh_token, expected_type="refresh")
        user_id_str = payload.get("sub")
        if not user_id_str:
            raise UnauthorizedException("Invalid token payload")

        try:
            user_id = UUID(str(user_id_str))
        except ValueError:
            raise UnauthorizedException("Invalid user ID in token")

        user = await self.repository.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User no longer active or found")

        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
