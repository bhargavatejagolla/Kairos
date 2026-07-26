from uuid import UUID

from app.core.exceptions import (
    CannotRemoveLastOwnerError,
    DuplicateMembershipError,
    MembershipNotFoundError,
)
from app.core.roles import RoleName
from app.db.models.organization_member import OrganizationMember
from app.repositories.organization_member import OrganizationMemberRepository
from app.repositories.role import RoleRepository


class MembershipService:
    def __init__(
        self,
        membership_repo: OrganizationMemberRepository,
        role_repo: RoleRepository,
    ) -> None:
        self.membership_repo = membership_repo
        self.role_repo = role_repo

    async def get_owner_role_id(self) -> UUID:
        role = await self.role_repo.get_by_name(RoleName.OWNER)
        if not role:
            raise RuntimeError("Owner role not found in database")
        return role.id

    async def _count_owners(self, org_id: UUID, owner_role_id: UUID) -> int:
        members = await self.membership_repo.list_members(org_id)
        return sum(1 for m in members if m.role_id == owner_role_id)

    async def add_member(
        self,
        org_id: UUID,
        user_id: UUID,
        role_id: UUID,
        invited_by_id: UUID | None = None,
    ) -> OrganizationMember:
        if await self.membership_repo.is_member(org_id, user_id):
            raise DuplicateMembershipError()

        member = OrganizationMember(
            organization_id=org_id,
            user_id=user_id,
            role_id=role_id,
            invited_by_id=invited_by_id,
        )
        return await self.membership_repo.add_member(member)

    async def remove_member(self, org_id: UUID, user_id: UUID) -> None:
        member = await self.membership_repo.get_member(org_id, user_id)
        if not member:
            raise MembershipNotFoundError()

        owner_role_id = await self.get_owner_role_id()
        if member.role_id == owner_role_id:
            owner_count = await self._count_owners(org_id, owner_role_id)
            if owner_count <= 1:
                raise CannotRemoveLastOwnerError()

        await self.membership_repo.remove_member(org_id, user_id)

    async def change_role(
        self, org_id: UUID, user_id: UUID, new_role_id: UUID
    ) -> OrganizationMember:
        member = await self.membership_repo.get_member(org_id, user_id)
        if not member:
            raise MembershipNotFoundError()

        owner_role_id = await self.get_owner_role_id()
        if member.role_id == owner_role_id and new_role_id != owner_role_id:
            owner_count = await self._count_owners(org_id, owner_role_id)
            if owner_count <= 1:
                raise CannotRemoveLastOwnerError(
                    "Cannot demote the last owner of an organization"
                )

        updated_member = await self.membership_repo.change_role(
            org_id, user_id, new_role_id
        )
        if not updated_member:
            raise MembershipNotFoundError()
        return updated_member

    async def transfer_ownership(
        self, org_id: UUID, current_owner_id: UUID, new_owner_id: UUID
    ) -> None:
        owner_role_id = await self.get_owner_role_id()
        admin_role = await self.role_repo.get_by_name(RoleName.ADMIN)
        if not admin_role:
            raise RuntimeError("Admin role not found in database")

        # Promote new owner
        new_owner_member = await self.membership_repo.get_member(org_id, new_owner_id)
        if not new_owner_member:
            raise MembershipNotFoundError()
            
        await self.membership_repo.change_role(org_id, new_owner_id, owner_role_id)
        
        # Demote current owner to admin
        await self.membership_repo.change_role(org_id, current_owner_id, admin_role.id)

    async def list_members(self, org_id: UUID) -> list[OrganizationMember]:
        return await self.membership_repo.list_members(org_id)
