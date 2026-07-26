from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.api.deps.services import get_user_service
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user import UserService

router = APIRouter()
UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    user_in: UserCreate,
    service: UserServiceDep,
) -> UserResponse:
    user = await service.create_user(user_in)
    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List all users",
)
async def list_users(
    service: UserServiceDep,
) -> list[UserResponse]:
    users = await service.list_users()
    return [UserResponse.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
)
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
) -> UserResponse:
    user = await service.get_user(user_id)
    return UserResponse.model_validate(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update user by ID",
)
async def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    service: UserServiceDep,
) -> UserResponse:
    user = await service.update_user(user_id, user_in)
    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by ID",
)
async def delete_user(
    user_id: UUID,
    service: UserServiceDep,
) -> None:
    await service.delete_user(user_id)
