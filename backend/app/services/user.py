from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import hash_password
from app.db.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service layer coordinating business rules and validation for Users."""

    def __init__(
        self,
        session_or_repo: AsyncSession | UserRepository,
    ) -> None:
        if isinstance(session_or_repo, AsyncSession):
            self.repository = UserRepository(session_or_repo)
        else:
            self.repository = session_or_repo
        self.user_repo = self.repository

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def get_user_by_id(self, user_id: UUID) -> User:
        return await self.get_user(user_id)

    async def list_users(self) -> list[User]:
        return await self.repository.get_all()

    async def get_all_users(self) -> list[User]:
        return await self.list_users()

    async def email_exists(self, email: str) -> bool:
        return await self.repository.email_exists(email)

    async def username_exists(self, username: str) -> bool:
        return await self.repository.username_exists(username)

    async def create_user(self, user_in: UserCreate) -> User:
        if await self.email_exists(user_in.email):
            raise UserAlreadyExistsError("User with this email already exists.")
        if await self.username_exists(user_in.username):
            raise UserAlreadyExistsError("User with this username already exists.")

        hashed_pw = hash_password(user_in.password)
        user_obj = User(
            email=user_in.email,
            username=user_in.username,
            full_name=user_in.full_name,
            hashed_password=hashed_pw,
            is_active=True,
        )
        user_created = await self.repository.create(user_obj)
        
        # Transactional Outbox for Domain Events
        from app.events.outbox_service import OutboxService
        from app.events.schema import DomainEvent
        from app.middleware.correlation import correlation_id_var
        
        # In user.py we might not have self.session explicitly, let's check
        # self.repository.session is available for sqlalchemy repos
        session = getattr(self.repository, "session", None)
        if session:
            outbox = OutboxService(session)
            event = DomainEvent(
                event_type="UserRegistered",
                resource_type="USER",
                resource_id=str(user_created.id),
                actor_id=str(user_created.id),
                correlation_id=correlation_id_var.get(None),
                payload={
                    "email": user_created.email,
                    "username": user_created.username,
                    "full_name": user_created.full_name
                }
            )
            await outbox.save_event(event)
        
        return user_created

    async def update_user(self, user_id: UUID, user_in: UserUpdate) -> User:
        user = await self.get_user(user_id)

        if user_in.email is not None and user_in.email != user.email:
            if await self.email_exists(user_in.email):
                raise UserAlreadyExistsError("User with this email already exists.")
            user.email = user_in.email

        if user_in.username is not None and user_in.username != user.username:
            if await self.username_exists(user_in.username):
                raise UserAlreadyExistsError("User with this username already exists.")
            user.username = user_in.username

        if user_in.full_name is not None:
            user.full_name = user_in.full_name

        if user_in.password is not None:
            user.hashed_password = hash_password(user_in.password)

        if user_in.is_active is not None:
            user.is_active = user_in.is_active

        return await self.repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        if not await self.repository.exists(user_id):
            raise UserNotFoundError()
        return await self.repository.delete(user_id)
