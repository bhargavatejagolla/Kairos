from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.core.security import get_password_hash


async def seed_default_user(db: AsyncSession) -> User:
    print("🌱 Seeding default user...")
    result = await db.execute(select(User).where(User.email == "admin@kairos.dev"))
    user = result.scalar_one_or_none()
    if not user:
        user = User(
            email="admin@kairos.dev",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("password123"),
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user
