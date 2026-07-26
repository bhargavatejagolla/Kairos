import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import Permission as PermissionEnum
from app.core.roles import RoleName
from app.db.models.permission import Permission
from app.db.models.role import Role
from app.db.session import SessionLocal

DEFAULT_ROLES_PERMISSIONS = {
    RoleName.OWNER: [
        PermissionEnum.USERS_READ,
        PermissionEnum.USERS_CREATE,
        PermissionEnum.USERS_UPDATE,
        PermissionEnum.USERS_DELETE,
        PermissionEnum.ORGANIZATIONS_READ,
        PermissionEnum.ORGANIZATIONS_CREATE,
        PermissionEnum.ORGANIZATIONS_UPDATE,
        PermissionEnum.ORGANIZATIONS_DELETE,
        PermissionEnum.PROJECTS_VIEW,
        PermissionEnum.PROJECTS_CREATE,
        PermissionEnum.PROJECTS_UPDATE,
        PermissionEnum.PROJECTS_ARCHIVE,
        PermissionEnum.PROJECTS_RESTORE,
        PermissionEnum.PROJECTS_DELETE,
        PermissionEnum.PROJECTS_SETTINGS_UPDATE,
        PermissionEnum.INCIDENTS_VIEW,
        PermissionEnum.INCIDENTS_CREATE,
        PermissionEnum.INCIDENTS_UPDATE,
        PermissionEnum.INCIDENTS_DELETE,
        PermissionEnum.ALERTS_READ,
        PermissionEnum.ALERTS_CREATE,
        PermissionEnum.ALERTS_UPDATE,
        PermissionEnum.ALERTS_DELETE,
        PermissionEnum.AI_ANALYZE,
        PermissionEnum.AUDIT_READ,
    ],
    RoleName.ADMIN: [
        PermissionEnum.USERS_READ,
        PermissionEnum.USERS_CREATE,
        PermissionEnum.USERS_UPDATE,
        PermissionEnum.USERS_DELETE,
        PermissionEnum.ORGANIZATIONS_READ,
        PermissionEnum.ORGANIZATIONS_CREATE,
        PermissionEnum.ORGANIZATIONS_UPDATE,
        PermissionEnum.ORGANIZATIONS_DELETE,
        PermissionEnum.PROJECTS_VIEW,
        PermissionEnum.PROJECTS_CREATE,
        PermissionEnum.PROJECTS_UPDATE,
        PermissionEnum.PROJECTS_ARCHIVE,
        PermissionEnum.PROJECTS_RESTORE,
        PermissionEnum.PROJECTS_SETTINGS_UPDATE,
        PermissionEnum.INCIDENTS_VIEW,
        PermissionEnum.INCIDENTS_CREATE,
        PermissionEnum.INCIDENTS_UPDATE,
        PermissionEnum.INCIDENTS_DELETE,
        PermissionEnum.ALERTS_READ,
        PermissionEnum.ALERTS_CREATE,
        PermissionEnum.ALERTS_UPDATE,
        PermissionEnum.ALERTS_DELETE,
        PermissionEnum.AI_ANALYZE,
        PermissionEnum.AUDIT_READ,
    ],
    RoleName.OPERATOR: [
        PermissionEnum.USERS_READ,
        PermissionEnum.PROJECTS_VIEW,
        PermissionEnum.PROJECTS_UPDATE,
        PermissionEnum.INCIDENTS_VIEW,
        PermissionEnum.INCIDENTS_UPDATE,
        PermissionEnum.ALERTS_READ,
        PermissionEnum.ALERTS_UPDATE,
        PermissionEnum.ALERTS_ACKNOWLEDGE,
        PermissionEnum.AI_ANALYZE,
    ],
    RoleName.DEVELOPER: [
        PermissionEnum.PROJECTS_VIEW,
        PermissionEnum.PROJECTS_CREATE,
        PermissionEnum.PROJECTS_UPDATE,
        PermissionEnum.INCIDENTS_VIEW,
        PermissionEnum.INCIDENTS_UPDATE,
        PermissionEnum.ALERTS_READ,
        PermissionEnum.AI_ANALYZE,
    ],
    RoleName.VIEWER: [
        PermissionEnum.USERS_READ,
        PermissionEnum.PROJECTS_VIEW,
        PermissionEnum.INCIDENTS_VIEW,
        PermissionEnum.ALERTS_READ,
    ],
}


async def seed_rbac(db: AsyncSession) -> None:
    print("Seeding RBAC data...")
    # 1. Ensure all permissions exist
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

    # 2. Ensure all roles exist and have correct permissions
    for role_name, perms in DEFAULT_ROLES_PERMISSIONS.items():
        # Handle cases where permission enums used in default map might not be in the enum due to updates (e.g. ALERTS_ACKNOWLEDGE)
        valid_perms = [
            p for p in perms if hasattr(p, "value") and p.value in db_permissions
        ]

        role_result = await db.execute(select(Role).where(Role.name == role_name.value))
        db_role = role_result.scalar_one_or_none()
        if not db_role:
            db_role = Role(
                name=role_name.value, description=f"{role_name.value.capitalize()} role"
            )
            db.add(db_role)
            await db.commit()
            await db.refresh(db_role)

        # Update role's permissions
        # We need to eager load permissions to update them properly
        from sqlalchemy.orm import selectinload

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

        # Optional: Remove extra permissions if we want strict syncing
        # For now, let's just ensure they have at least the defaults

        await db.commit()
    print("RBAC seeding complete.")


async def main() -> None:
    async with SessionLocal() as session:
        await seed_rbac(session)


if __name__ == "__main__":
    asyncio.run(main())
