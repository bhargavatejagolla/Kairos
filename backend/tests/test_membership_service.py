from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import CannotRemoveLastOwnerError
from app.db.models.organization_member import OrganizationMember
from app.db.models.role import Role
from app.services.membership_service import MembershipService


@pytest.fixture
def mock_membership_repo():
    return AsyncMock()


@pytest.fixture
def mock_role_repo():
    return AsyncMock()


@pytest.mark.anyio
async def test_remove_last_owner(mock_membership_repo, mock_role_repo):
    org_id = uuid4()
    user_id = uuid4()
    owner_role_id = uuid4()
    
    mock_role_repo.get_by_name.return_value = Role(id=owner_role_id, name="owner")
    
    member = OrganizationMember(
        id=uuid4(),
        organization_id=org_id,
        user_id=user_id,
        role_id=owner_role_id
    )
    
    mock_membership_repo.get_member.return_value = member
    mock_membership_repo.list_members.return_value = [member]
    
    service = MembershipService(mock_membership_repo, mock_role_repo)
    
    with pytest.raises(CannotRemoveLastOwnerError):
        await service.remove_member(org_id, user_id)


@pytest.mark.anyio
async def test_transfer_ownership(mock_membership_repo, mock_role_repo):
    org_id = uuid4()
    current_owner_id = uuid4()
    new_owner_id = uuid4()
    owner_role_id = uuid4()
    admin_role_id = uuid4()
    
    mock_role_repo.get_by_name.side_effect = lambda name: Role(id=owner_role_id, name="owner") if name == "owner" else Role(id=admin_role_id, name="admin")
    
    new_owner_member = OrganizationMember(
        id=uuid4(),
        organization_id=org_id,
        user_id=new_owner_id,
        role_id=admin_role_id
    )
    
    mock_membership_repo.get_member.return_value = new_owner_member
    
    service = MembershipService(mock_membership_repo, mock_role_repo)
    
    await service.transfer_ownership(org_id, current_owner_id, new_owner_id)
    
    # Should be called twice: promote new, demote old
    assert mock_membership_repo.change_role.call_count == 2
