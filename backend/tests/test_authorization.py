from unittest.mock import patch
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


def test_permission_allowed(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(auth_service, "has_permission") as mock_has_perm:
        mock_has_perm.return_value = True

        # Should not raise
        auth_service.require_permission(normal_user, "users:read")
        mock_has_perm.assert_called_once_with(normal_user, "users:read")


def test_permission_denied(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(auth_service, "has_permission") as mock_has_perm:
        mock_has_perm.return_value = False

        with pytest.raises(PermissionDeniedError) as exc:
            auth_service.require_permission(normal_user, "users:read")

        assert exc.value.status_code == 403
        assert exc.value.detail == "Permission denied: users:read"


def test_unknown_permission(
    auth_service: AuthorizationService, normal_user: User
) -> None:
    with patch.object(auth_service, "has_permission") as mock_has_perm:
        mock_has_perm.return_value = False

        has_perm = auth_service.has_permission(
            normal_user, "does_not_exist:write"
        )
        assert has_perm is False
