from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.core.exceptions import OrganizationAlreadyExistsError, ReservedSlugError
from app.db.models.organization import Organization
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import OrganizationService


@pytest.fixture
def mock_org_repo():
    repo = AsyncMock()
    repo.exists_slug.return_value = False
    return repo


@pytest.fixture
def mock_membership_service():
    service = AsyncMock()
    service.get_owner_role_id.return_value = uuid4()
    return service


@pytest.mark.anyio
async def test_create_organization(mock_org_repo, mock_membership_service):
    user_id = uuid4()
    org_id = uuid4()
    
    mock_org = Organization(
        id=org_id,
        name="Test Org",
        slug="test-org",
        created_by_id=user_id,
    )
    mock_org_repo.create.return_value = mock_org
    mock_org_repo.get_by_id.return_value = mock_org

    service = OrganizationService(mock_org_repo, mock_membership_service)
    data = OrganizationCreate(name="Test Org", slug="test-org")
    
    result = await service.create_organization(data, user_id)
    
    assert result.id == org_id
    mock_membership_service.add_member.assert_called_once()
    mock_org_repo.create.assert_called_once()


@pytest.mark.anyio
async def test_create_organization_reserved_slug(mock_org_repo, mock_membership_service):
    service = OrganizationService(mock_org_repo, mock_membership_service)
    data = OrganizationCreate(name="Admin", slug="admin")
    
    with pytest.raises(ReservedSlugError):
        await service.create_organization(data, uuid4())


@pytest.mark.anyio
async def test_create_organization_duplicate_slug(mock_org_repo, mock_membership_service):
    mock_org_repo.exists_slug.return_value = True
    service = OrganizationService(mock_org_repo, mock_membership_service)
    data = OrganizationCreate(name="Test Org", slug="test-org")
    
    with pytest.raises(OrganizationAlreadyExistsError):
        await service.create_organization(data, uuid4())
