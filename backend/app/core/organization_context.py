from dataclasses import dataclass

from app.db.models.organization import Organization
from app.db.models.organization_member import OrganizationMember
from app.db.models.role import Role


@dataclass
class OrganizationContext:
    organization: Organization
    membership: OrganizationMember

    @property
    def role(self) -> Role:
        return self.membership.role
