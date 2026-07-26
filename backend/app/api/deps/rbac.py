from typing import Annotated, Any

from fastapi import Depends

from app.api.deps.organization import OrganizationContextDep
from app.api.deps.services import get_authorization_service
from app.core.organization_context import OrganizationContext
from app.services.authorization import AuthorizationService


class RequirePermission:
    """
    Dependency to check if the current user has the required permission
    within the current organization context.

    Delegates the actual check to AuthorizationService.
    """

    def __init__(self, required_permission: str) -> None:
        self.required_permission = required_permission

    def __call__(
        self,
        context: OrganizationContextDep,
        auth_service: Annotated[
            AuthorizationService, Depends(get_authorization_service)
        ],
    ) -> OrganizationContext:
        auth_service.require_permission(
            context=context,
            permission=self.required_permission,
        )
        return context


def require_permission(permission: str) -> Any:
    return RequirePermission(permission)
