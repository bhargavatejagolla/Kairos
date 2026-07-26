from pydantic import ConfigDict, EmailStr

from app.schemas.base import SchemaBase
from app.schemas.user import UserResponse


class LoginRequest(SchemaBase):
    email: EmailStr
    password: str


class TokenResponse(SchemaBase):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(SchemaBase):
    refresh_token: str


class LogoutRequest(SchemaBase):
    refresh_token: str


class ChangePasswordRequest(SchemaBase):
    current_password: str
    new_password: str


class CurrentUserResponse(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    user: UserResponse
