from fastapi import HTTPException


class ResourceNotFoundException(HTTPException):
    def __init__(self, resource: str) -> None:
        super().__init__(
            status_code=404,
            detail=f"{resource} not found",
        )


class BadRequestException(HTTPException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=400,
            detail=message,
        )


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Unauthorized") -> None:
        super().__init__(
            status_code=401,
            detail=detail,
        )


class DuplicateResourceException(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=409,
            detail=detail,
        )


class UserNotFoundError(ResourceNotFoundException):
    def __init__(self) -> None:
        super().__init__("User")


class UserAlreadyExistsError(DuplicateResourceException):
    def __init__(self, detail: str = "User already exists") -> None:
        super().__init__(detail)


class InvalidCredentialsError(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid credentials")


class PermissionDeniedError(HTTPException):
    def __init__(self, detail: str = "Permission denied") -> None:
        super().__init__(
            status_code=403,
            detail=detail,
        )
