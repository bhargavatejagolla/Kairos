from collections.abc import AsyncGenerator
from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool

from app.core.exceptions import DuplicateResourceException, ResourceNotFoundException
from app.core.security import verify_password
from app.db.base import Base
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
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
async def test_user_service_crud_and_validation(db_session: AsyncSession) -> None:
    repo = UserRepository(db_session)
    service = UserService(repo)

    # 1. Create User
    user_in = UserCreate(
        email="john@example.com",
        username="johndoe",
        full_name="John Doe",
        password="secretpassword123",
    )
    user = await service.create_user(user_in)
    assert user.id is not None
    assert user.email == "john@example.com"
    assert user.username == "johndoe"
    assert user.full_name == "John Doe"
    assert user.is_active is True
    assert user.hashed_password.startswith("$argon2")
    assert verify_password("secretpassword123", user.hashed_password) is True
    assert verify_password("wrongpassword", user.hashed_password) is False

    # 2. Test Duplicate Email on Create
    dup_email_in = UserCreate(
        email="john@example.com",
        username="differentuser",
        full_name="Different User",
        password="anotherpassword123",
    )
    with pytest.raises(DuplicateResourceException) as exc_info:
        await service.create_user(dup_email_in)
    assert "email already exists" in str(exc_info.value.detail)

    # 3. Test Duplicate Username on Create
    dup_username_in = UserCreate(
        email="different@example.com",
        username="johndoe",
        full_name="Different User",
        password="anotherpassword123",
    )
    with pytest.raises(DuplicateResourceException) as exc_info:
        await service.create_user(dup_username_in)
    assert "username already exists" in str(exc_info.value.detail)

    # Create a second user for update duplicate testing
    user2_in = UserCreate(
        email="alice@example.com",
        username="alice",
        full_name="Alice Smith",
        password="alicepassword123",
    )
    await service.create_user(user2_in)

    # 4. Get User by ID & Not Found
    fetched = await service.get_user_by_id(user.id)
    assert fetched.email == user.email

    with pytest.raises(ResourceNotFoundException):
        await service.get_user_by_id(uuid4())

    # 5. List Users
    users = await service.get_all_users()
    assert len(users) == 2

    # 6. Update User (full_name, password, is_active, email, username)
    update_in = UserUpdate(
        email="john_new@example.com",
        username="johndoe_new",
        full_name="John Updated",
        password="newsecretpassword456",
        is_active=False,
    )
    updated = await service.update_user(user.id, update_in)
    assert updated.email == "john_new@example.com"
    assert updated.username == "johndoe_new"
    assert updated.full_name == "John Updated"
    assert updated.is_active is False
    assert verify_password("newsecretpassword456", updated.hashed_password) is True

    # Test duplicate email on update
    with pytest.raises(DuplicateResourceException):
        await service.update_user(user.id, UserUpdate(email="alice@example.com"))

    # Test duplicate username on update
    with pytest.raises(DuplicateResourceException):
        await service.update_user(user.id, UserUpdate(username="alice"))

    # 7. Delete User & Not Found
    await service.delete_user(user.id)
    with pytest.raises(ResourceNotFoundException):
        await service.get_user_by_id(user.id)

    with pytest.raises(ResourceNotFoundException):
        await service.delete_user(user.id)
