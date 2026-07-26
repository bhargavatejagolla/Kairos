from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.deps.auth import ActiveUserDep
from app.api.deps.services import get_auth_service
from app.schemas.auth import (
    ChangePasswordRequest,
    CurrentUserResponse,
    LoginRequest,
    LogoutRequest,
    RefreshTokenRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter()
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login to obtain access and refresh tokens",
)
async def login(
    login_in: LoginRequest,
    service: AuthServiceDep,
) -> TokenResponse:
    return await service.login(login_in)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token using valid refresh token",
)
async def refresh_token(
    refresh_in: RefreshTokenRequest,
    service: AuthServiceDep,
) -> TokenResponse:
    return await service.refresh_tokens(refresh_in.refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Revoke refresh token to terminate user session",
)
async def logout(
    logout_in: LogoutRequest,
    service: AuthServiceDep,
) -> dict[str, Any]:
    await service.logout(logout_in.refresh_token)
    return {"message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=CurrentUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
)
async def get_current_user_profile(
    current_user: ActiveUserDep,
) -> CurrentUserResponse:
    return CurrentUserResponse(user=UserResponse.model_validate(current_user))


@router.post(
    "/change-password",
    status_code=status.HTTP_200_OK,
    summary="Change current authenticated user password",
)
async def change_password(
    change_in: ChangePasswordRequest,
    current_user: ActiveUserDep,
    service: AuthServiceDep,
) -> dict[str, Any]:
    await service.change_password(
        current_user.id, change_in.current_password, change_in.new_password
    )
    return {"message": "Password changed successfully"}
