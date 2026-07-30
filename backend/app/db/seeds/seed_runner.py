import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.permissions import Permission as PermissionEnum
from app.core.roles import RoleName
from app.db.models.permission import Permission
from app.db.models.role import Role
from app.db.seeds.rbac import DEFAULT_ROLES_PERMISSIONS
from app.db.session import SessionLocal


async def seed_permissions(db: AsyncSession) -> dict[str, Permission]:
    print("Seeding permissions...")
    db_permissions = {}
    for perm_enum in PermissionEnum:
        result = await db.execute(
            select(Permission).where(Permission.name == perm_enum.value)
        )
        perm = result.scalar_one_or_none()
        if not perm:
            perm = Permission(
                name=perm_enum.value, description=f"Allows {perm_enum.value}"
            )
            db.add(perm)
        db_permissions[perm_enum.value] = perm
    await db.commit()
    return db_permissions


async def seed_default_roles(db: AsyncSession) -> dict[str, Role]:
    print("Seeding default roles...")
    db_roles = {}
    for role_name in RoleName:
        role_result = await db.execute(select(Role).where(Role.name == role_name.value))
        db_role = role_result.scalar_one_or_none()
        if not db_role:
            db_role = Role(
                name=role_name.value, description=f"{role_name.value.capitalize()} role"
            )
            db.add(db_role)
            await db.commit()
            await db.refresh(db_role)
        db_roles[role_name.value] = db_role
    return db_roles


async def connect_roles_permissions(
    db: AsyncSession, db_roles: dict[str, Role], db_permissions: dict[str, Permission]
) -> None:
    print("Connecting roles and permissions...")
    for role_name, perms in DEFAULT_ROLES_PERMISSIONS.items():
        valid_perms = [
            p for p in perms if hasattr(p, "value") and p.value in db_permissions
        ]

        db_role = db_roles[role_name.value]

        role_with_perms_result = await db.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.id == db_role.id)
        )
        role_with_perms = role_with_perms_result.scalar_one()

        current_perm_names = {p.name for p in role_with_perms.permissions}
        target_perm_names = {p.value for p in valid_perms}

        # Add missing permissions
        for perm_name in target_perm_names - current_perm_names:
            role_with_perms.permissions.append(db_permissions[perm_name])

    await db.commit()


async def seed_rbac(db: AsyncSession) -> None:
    print("Starting RBAC seeding...")
    db_permissions = await seed_permissions(db)
    db_roles = await seed_default_roles(db)
    await connect_roles_permissions(db, db_roles, db_permissions)
    print("RBAC seeding complete.")


async def main() -> None:
    from app.db.seeds.organization import seed_development_organization
    from app.db.seeds.user import seed_default_user
    from app.repositories.organization import OrganizationRepository
    from app.repositories.organization_member import OrganizationMemberRepository
    from app.repositories.role import RoleRepository
    from app.services.membership_service import MembershipService
    from app.services.organization_service import OrganizationService

    async with SessionLocal() as session:
        await seed_rbac(session)
        user = await seed_default_user(session)

        # Setup services for Organization seeding
        role_repo = RoleRepository(session)
        membership_repo = OrganizationMemberRepository(session)
        membership_service = MembershipService(membership_repo, role_repo)
        
        org_repo = OrganizationRepository(session)
        org_service = OrganizationService(org_repo, membership_service)

        await seed_development_organization(session, user, org_service)
        
        # Seed Projects and Incident Domain
        from app.db.seeds.incident import seed_incident_domain
        from app.db.seeds.project import seed_projects
        await seed_projects(session)
        await seed_incident_domain(session)
        
        # We must commit at the very end since the services use flush
        await session.commit()
        print("✅ All seeds completed successfully.")


if __name__ == "__main__":
    asyncio.run(main())
