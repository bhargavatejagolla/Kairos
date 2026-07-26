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


class RoleNotFoundError(HTTPException):
    def __init__(self, detail: str = "Role not found") -> None:
        super().__init__(status_code=404, detail=detail)


class PermissionNotFoundError(HTTPException):
    def __init__(self, detail: str = "Permission not found") -> None:
        super().__init__(status_code=404, detail=detail)


class RoleAlreadyExistsError(HTTPException):
    def __init__(self, detail: str = "Role already exists") -> None:
        super().__init__(status_code=400, detail=detail)


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


class OrganizationNotFoundError(ResourceNotFoundException):
    def __init__(self) -> None:
        super().__init__("Organization")


class OrganizationAlreadyExistsError(DuplicateResourceException):
    def __init__(self, detail: str = "Organization already exists") -> None:
        super().__init__(detail)


class MembershipNotFoundError(ResourceNotFoundException):
    def __init__(self) -> None:
        super().__init__("Organization Member")


class DuplicateMembershipError(DuplicateResourceException):
    def __init__(self, detail: str = "User is already a member of this organization") -> None:
        super().__init__(detail)


class CannotRemoveLastOwnerError(BadRequestException):
    def __init__(self, detail: str = "Cannot remove the last owner of an organization") -> None:
        super().__init__(detail)


class ReservedSlugError(BadRequestException):
    def __init__(self, detail: str = "Organization slug is reserved") -> None:
        super().__init__(detail)


# Project Domain Exceptions
class EnvironmentNotFoundError(ResourceNotFoundException):
    def __init__(self) -> None:
        super().__init__("Environment")


class EnvironmentInUseError(BadRequestException):
    def __init__(self) -> None:
        super().__init__("Environment is currently in use by projects")


class ProjectNotFoundError(ResourceNotFoundException):
    def __init__(self, detail: str = "Project") -> None:
        super().__init__(detail)


class ProjectAlreadyExistsError(DuplicateResourceException):
    def __init__(self) -> None:
        super().__init__("Project with this slug already exists in the organization")


class ProjectArchivedError(BadRequestException):
    def __init__(self) -> None:
        super().__init__("Project is archived and cannot be modified")


class InvalidProjectStateError(BadRequestException):
    def __init__(self, detail: str) -> None:
        super().__init__(detail)
