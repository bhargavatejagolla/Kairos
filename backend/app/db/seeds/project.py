import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.project import ProjectStatus, ProjectVisibility
from app.db.models.environment import Environment
from app.db.models.organization import Organization
from app.db.models.project import Project
from app.db.models.project_settings import ProjectSettings
from app.db.models.user import User
from app.db.session import SessionLocal


async def seed_projects(db: AsyncSession) -> None:
    print("Seeding environments and projects...")

    # Fetch all organizations
    orgs = (await db.execute(select(Organization))).scalars().all()
    users = (await db.execute(select(User))).scalars().all()
    
    if not orgs or not users:
        print("No organizations or users found. Skipping project seed.")
        return

    admin_user = users[0]

    for org in orgs:
        # Create Environments
        environments = []
        for name, slug, color in [("Production", "production", "red"), ("Staging", "staging", "yellow"), ("Development", "development", "green")]:
            env = (await db.execute(select(Environment).where(Environment.organization_id == org.id, Environment.slug == slug))).scalar_one_or_none()
            if not env:
                env = Environment(organization_id=org.id, name=name, slug=slug, color=color)
                db.add(env)
            environments.append(env)
            
        await db.commit()
        
        # Make sure they have IDs
        for env in environments:
            await db.refresh(env)

        # Create a sample Project
        project_slug = "payment-api"
        project = (await db.execute(select(Project).where(Project.organization_id == org.id, Project.slug == project_slug))).scalar_one_or_none()
        
        if not project:
            project = Project(
                organization_id=org.id,
                environment_id=environments[0].id,
                name="Payment API",
                slug=project_slug,
                description="Core payment processing service",
                status=ProjectStatus.ACTIVE,
                visibility=ProjectVisibility.PRIVATE,
                created_by_id=admin_user.id,
                updated_by_id=admin_user.id
            )
            db.add(project)
            await db.commit()
            await db.refresh(project)
            
            # Create settings
            settings = ProjectSettings(project_id=project.id)
            db.add(settings)
            await db.commit()

    print("Project seeding complete.")


async def main() -> None:
    async with SessionLocal() as session:
        await seed_projects(session)


if __name__ == "__main__":
    asyncio.run(main())
