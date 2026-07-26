from uuid import UUID

from app.core.exceptions import PermissionDeniedError
from app.core.organization_context import OrganizationContext
from app.db.models.user import User


class AuthorizationService:
    """
    Authorization Engine for KAIROS.

    This service evaluates if the given context satisfies
    a specific permission requirement.
    """

    def __init__(self) -> None:
        pass

    def has_permission(
        self,
        context: OrganizationContext,
        permission: str,
    ) -> bool:
        """
        Check if an organization context has a specific permission.

        Args:
            context: The validated organization context for the current user.
            permission: The required permission string.

        Returns:
            True if the role possesses the permission.
        """
        for perm in context.role.permissions:
            if perm.name == permission:
                return True
        return False

    def require_permission(
        self,
        context: OrganizationContext,
        permission: str,
    ) -> bool:
        """
        Convenience method that raises an exception if permission is denied.
        """
        has_perm = self.has_permission(context, permission)
        if not has_perm:
            raise PermissionDeniedError(f"Permission denied: {permission}")
        return True
