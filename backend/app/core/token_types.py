from enum import StrEnum


class TokenType(StrEnum):
    """Enumeration of token types used in the authentication system."""

    ACCESS = "access"
    REFRESH = "refresh"
    BEARER = "bearer"
