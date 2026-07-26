from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidCredentialsError,
    UnauthorizedException,
)
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    get_token_expiration,
    get_token_jti,
    verify_token,
)
from app.core.security import hash_password, verify_password
from app.core.token_types import TokenType
from app.repositories.token_repository import TokenRepository
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse


class AuthService:
    """Service layer handling authentication, token issuance, rotation, and validation."""

    def __init__(
        self,
        session_or_repo: AsyncSession | UserRepository,
        token_repository: TokenRepository | None = None,
    ) -> None:
        if isinstance(session_or_repo, AsyncSession):
            self.repository = UserRepository(session_or_repo)
            self.token_repository: TokenRepository | None = TokenRepository(
                session_or_repo
            )
        else:
            self.repository = session_or_repo
            self.token_repository = token_repository

        self.users = self.repository
        self.sessions = self.token_repository

    async def login(
        self,
        login_in: LoginRequest,
        *,
        user_agent: str | None = None,
        ip_address: str | None = None,
    ) -> TokenResponse:
        """Authenticate user by email/password and issue JWT token pair with session tracking."""
        user = await self.repository.get_by_email(login_in.email)
        if not user:
            raise InvalidCredentialsError()

        if not verify_password(login_in.password, user.hashed_password):
            raise InvalidCredentialsError()

        if not user.is_active:
            raise UnauthorizedException("User account is inactive")

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)

        if self.token_repository:
            jti = get_token_jti(refresh_token)
            exp = get_token_expiration(refresh_token)
            await self.token_repository.create_token(
                user_id=user.id,
                token_id=jti,
                expires_at=exp,
                user_agent=user_agent,
                ip_address=ip_address,
            )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=TokenType.BEARER,
        )

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """Verify refresh token, perform rotation, detect reuse, and issue a new JWT token pair."""
        payload = verify_token(refresh_token, expected_type=TokenType.REFRESH)
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

        if self.token_repository:
            jti = get_token_jti(refresh_token)
            token_record = await self.token_repository.get_by_jti(jti)
            if not token_record:
                raise UnauthorizedException("Refresh token unrecognized")

            if token_record.revoked:
                # Security event: compromised token reuse attempt! Revoke all active sessions.
                await self.token_repository.revoke_all_for_user(user.id)
                raise UnauthorizedException(
                    "Refresh token revoked; all sessions terminated"
                )

            expires_at = token_record.expires_at
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=UTC)
            if expires_at <= datetime.now(UTC):
                raise UnauthorizedException("Refresh token expired in database")

            # Rotate out old refresh token
            await self.token_repository.revoke_by_jti(jti)

        new_access_token = create_access_token(subject=user.id)
        new_refresh_token = create_refresh_token(subject=user.id)

        if self.token_repository:
            new_jti = get_token_jti(new_refresh_token)
            new_exp = get_token_expiration(new_refresh_token)
            await self.token_repository.create_token(
                user_id=user.id, token_id=new_jti, expires_at=new_exp
            )

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type=TokenType.BEARER,
        )

    async def logout(self, refresh_token: str) -> bool:
        """Revoke a refresh token to end the user's session."""
        try:
            jti = get_token_jti(refresh_token)
        except UnauthorizedException:
            return False

        if self.token_repository:
            return await self.token_repository.revoke_by_jti(jti)
        return True

    async def logout_all(self, user_id: UUID) -> int:
        """Revoke all active refresh tokens for a user across all devices."""
        if self.token_repository:
            return await self.token_repository.revoke_all_for_user(user_id)
        return 0

    async def change_password(
        self, user_id: UUID, current_password: str, new_password: str
    ) -> bool:
        """Change user password after verifying current password, and revoke existing sessions."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found")

        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError()

        user.hashed_password = hash_password(new_password)
        await self.repository.update(user)

        if self.token_repository:
            await self.token_repository.revoke_all_for_user(user_id)

        return True
