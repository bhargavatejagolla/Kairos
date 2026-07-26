from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user import User
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import OrganizationService


async def seed_development_organization(
    db: AsyncSession,
    owner_user: User,
    organization_service: OrganizationService,
) -> None:
    """
    Seed a development organization and attach the provided user as the owner.
    """
    if await organization_service.org_repo.exists_slug("development"):
        return

    print("🌱 Seeding Development Organization...")
    org_data = OrganizationCreate(
        name="Development Organization",
        slug="development",
        description="The default organization for development purposes.",
    )
    
    await organization_service.create_organization(data=org_data, user_id=owner_user.id)
