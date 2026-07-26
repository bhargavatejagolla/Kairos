from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.core.exceptions import InvalidCredentialsError, UnauthorizedException
from app.db.base import Base
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserUpdate
from app.services.auth_service import AuthService
from app.services.user import UserService

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.mark.anyio
async def test_auth_service_unit(db_session: AsyncSession) -> None:
    user_repo = UserRepository(db_session)
    user_service = UserService(user_repo)
    auth_service = AuthService(db_session)

    # 1. Create a user
    user = await user_service.create_user(
        UserCreate(
            email="authunit@example.com",
            username="authunit",
            full_name="Auth Unit",
            password="unitpassword123",
        )
    )

    # 2. Test successful login
    token_res = await auth_service.login(
        LoginRequest(email="authunit@example.com", password="unitpassword123")
    )
    assert token_res.access_token is not None
    assert token_res.refresh_token is not None

    # 3. Test wrong password
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            LoginRequest(email="authunit@example.com", password="wrongpassword")
        )

    # 4. Test nonexistent user
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            LoginRequest(email="nobody@example.com", password="unitpassword123")
        )

    # 5. Test refresh tokens success
    ref_res = await auth_service.refresh_tokens(token_res.refresh_token)
    assert ref_res.access_token != token_res.access_token

    # 6. Test refresh token with invalid string
    with pytest.raises(UnauthorizedException):
        await auth_service.refresh_tokens("invalid.token")

    # 7. Test inactive user login & refresh
    await user_service.update_user(user.id, UserUpdate(is_active=False))

    with pytest.raises(UnauthorizedException, match="inactive"):
        await auth_service.login(
            LoginRequest(email="authunit@example.com", password="unitpassword123")
        )

    with pytest.raises(UnauthorizedException, match="no longer active"):
        await auth_service.refresh_tokens(token_res.refresh_token)

    # 8. Test initializing AuthService with UserRepository directly
    auth_service_repo = AuthService(user_repo)
    assert auth_service_repo.repository == user_repo

    # 9. Test refresh token with missing 'sub'
    from app.core.jwt import create_refresh_token, jwt, settings

    token_missing_sub = jwt.encode(
        {"type": "refresh"}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    with pytest.raises(UnauthorizedException, match="Invalid token payload"):
        await auth_service.refresh_tokens(token_missing_sub)

    # 10. Test refresh token with non-UUID 'sub'
    token_bad_uuid = create_refresh_token(subject="not-a-uuid")
    with pytest.raises(UnauthorizedException, match="Invalid user ID in token"):
        await auth_service.refresh_tokens(token_bad_uuid)

    # 11. Test refresh token for a user that was deleted from database
    token_deleted_user = create_refresh_token(subject=uuid4())
    with pytest.raises(UnauthorizedException, match="User no longer active or found"):
        await auth_service.refresh_tokens(token_deleted_user)

    # 12. Test Refresh Token Rotation reuse detection (security event)
    await user_service.update_user(user.id, UserUpdate(is_active=True))
    fresh_login = await auth_service.login(
        LoginRequest(email="authunit@example.com", password="unitpassword123")
    )
    rotated_res = await auth_service.refresh_tokens(fresh_login.refresh_token)
    assert rotated_res.access_token is not None

    # Attempting to reuse the rotated out refresh token should trigger reuse detection and revoke all sessions!
    with pytest.raises(UnauthorizedException, match="terminated"):
        await auth_service.refresh_tokens(fresh_login.refresh_token)

    # Even the new rotated token should now be revoked due to the security event!
    with pytest.raises(UnauthorizedException, match="terminated|unrecognized"):
        await auth_service.refresh_tokens(rotated_res.refresh_token)

    # 13. Test logout
    login_for_logout = await auth_service.login(
        LoginRequest(email="authunit@example.com", password="unitpassword123")
    )
    assert await auth_service.logout(login_for_logout.refresh_token) is True
    with pytest.raises(UnauthorizedException):
        await auth_service.refresh_tokens(login_for_logout.refresh_token)

    # 14. Test change password
    with pytest.raises(InvalidCredentialsError):
        await auth_service.change_password(user.id, "wrongold", "newpass123")
    assert (
        await auth_service.change_password(user.id, "unitpassword123", "newpass123")
        is True
    )
    # Login with old password should fail, new password should succeed
    with pytest.raises(InvalidCredentialsError):
        await auth_service.login(
            LoginRequest(email="authunit@example.com", password="unitpassword123")
        )
    new_login = await auth_service.login(
        LoginRequest(email="authunit@example.com", password="newpass123")
    )
    assert new_login.access_token is not None

    # 15. Test validate_password_strength
    from app.core.security import validate_password_strength

    assert validate_password_strength("1234567") is False
    assert validate_password_strength("12345678") is True
