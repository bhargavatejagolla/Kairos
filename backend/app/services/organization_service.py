from uuid import UUID

from app.core.exceptions import OrganizationAlreadyExistsError, OrganizationNotFoundError, ReservedSlugError
from app.db.models.organization import Organization
from app.repositories.organization import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.services.membership_service import MembershipService


class OrganizationService:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        membership_service: MembershipService,
    ) -> None:
        self.org_repo = org_repo
        self.membership_service = membership_service
        self.reserved_slugs = {"admin", "system", "api", "login", "docs"}

    async def _validate_slug(self, slug: str) -> None:
        if slug.lower() in self.reserved_slugs:
            raise ReservedSlugError()
        if await self.org_repo.exists_slug(slug):
            raise OrganizationAlreadyExistsError()

    async def create_organization(
        self, data: OrganizationCreate, user_id: UUID
    ) -> Organization:
        await self._validate_slug(data.slug)

        org = Organization(
            name=data.name,
            slug=data.slug,
            description=data.description,
            website=data.website,
            logo_url=data.logo_url,
            created_by_id=user_id,
        )

        created_org = await self.org_repo.create(org)

        owner_role_id = await self.membership_service.get_owner_role_id()
        await self.membership_service.add_member(
            org_id=created_org.id,
            user_id=user_id,
            role_id=owner_role_id,
        )

        org = await self.get_organization(created_org.id)
        await self.org_repo.session.refresh(org)
        return org

    async def get_organization(self, org_id: UUID) -> Organization:
        org = await self.org_repo.get_by_id(org_id)
        if not org:
            raise OrganizationNotFoundError()
        return org

    async def update_organization(
        self, org_id: UUID, data: OrganizationUpdate
    ) -> Organization:
        org = await self.get_organization(org_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(org, key, value)

        await self.org_repo.session.flush()
        await self.org_repo.session.refresh(org)
        return org

    async def delete_organization(self, org_id: UUID) -> None:
        org = await self.get_organization(org_id)
        await self.org_repo.delete(org.id)

    async def list_organizations(self) -> list[Organization]:
        # Using pagination in future, but listing all for now
        return await self.org_repo.list()
