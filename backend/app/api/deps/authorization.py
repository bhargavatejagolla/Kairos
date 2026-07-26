from typing import Callable, Coroutine, Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.services import get_authorization_service
from app.core.permissions import Permission
from app.core.service_context import ServiceContext
from app.core.project_context import ProjectContext
from app.services.authorization import AuthorizationService
from app.api.deps.service import get_service_context
from app.api.deps.project import get_project_context

def require_incident_permission(permission: Permission) -> Callable:
    """
    Dependency generator that checks if the current user has the specified 
    permission for incidents within the given service context.
    """
    async def permission_checker(
        ctx: ServiceContext = Depends(get_service_context),
        authz_service: AuthorizationService = Depends(get_authorization_service)
    ) -> ServiceContext:
        if not ctx.member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this organization",
            )
            
        has_permission = authz_service.has_permission(ctx.role, permission)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required permission: {permission}",
            )
            
        return ctx

    return permission_checker
    
def require_service_permission(permission: Permission) -> Callable:
    """
    Dependency generator for service-level permissions.
    """
    async def permission_checker(
        ctx: ProjectContext = Depends(get_project_context),
        authz_service: AuthorizationService = Depends(get_authorization_service)
    ) -> ProjectContext:
        if not ctx.member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a member of this organization",
            )
            
        has_permission = authz_service.has_permission(ctx.role, permission)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User lacks required permission: {permission}",
            )
            
        return ctx

    return permission_checker
