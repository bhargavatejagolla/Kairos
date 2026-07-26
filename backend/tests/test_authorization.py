from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.core.exceptions import PermissionDeniedError
from app.db.models.user import User
from app.services.authorization import AuthorizationService


@pytest.fixture
def auth_service() -> AuthorizationService:
    return AuthorizationService()


@pytest.fixture
def normal_user() -> User:
    return User(
        id=uuid4(),
        email="normal@example.com",
        username="normaluser",
    )


@pytest.mark.anyio
async def test_permission_allowed(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(
        auth_service, "has_permission", new_callable=AsyncMock
    ) as mock_has_perm:
        mock_has_perm.return_value = True

        # Should not raise
        await auth_service.require_permission(normal_user, "users:read")
        mock_has_perm.assert_called_once_with(normal_user, "users:read", None)


@pytest.mark.anyio
async def test_permission_denied(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(
        auth_service, "has_permission", new_callable=AsyncMock
    ) as mock_has_perm:
        mock_has_perm.return_value = False

        with pytest.raises(PermissionDeniedError) as exc:
            await auth_service.require_permission(normal_user, "users:read")

        assert exc.value.status_code == 403
        assert exc.value.detail == "Permission denied: users:read"


@pytest.mark.anyio
async def test_unknown_permission(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(
        auth_service, "has_permission", new_callable=AsyncMock
    ) as mock_has_perm:
        mock_has_perm.return_value = False

        has_perm = await auth_service.has_permission(
            normal_user, "does_not_exist:write"
        )
        assert has_perm is False
