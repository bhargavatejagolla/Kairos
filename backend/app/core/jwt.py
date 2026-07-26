from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4

import jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedException
from app.core.token_types import TokenType


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """Create a new JWT access token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = {
        "exp": expire,
        "iat": now,
        "jti": str(uuid4()),
        "sub": str(subject),
        "type": TokenType.ACCESS,
    }
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def create_refresh_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """Create a new JWT refresh token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.refresh_token_expire_days)
    to_encode = {
        "exp": expire,
        "iat": now,
        "jti": str(uuid4()),
        "sub": str(subject),
        "type": TokenType.REFRESH,
    }
    return jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode a JWT token and handle signature or expiration errors."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError:
        raise UnauthorizedException("Invalid token")


def verify_token(token: str, expected_type: str = TokenType.ACCESS) -> dict[str, Any]:
    """Verify a token is valid and of the expected type ('access' or 'refresh')."""
    payload = decode_token(token)
    token_type = payload.get("type")
    if token_type != expected_type:
        raise UnauthorizedException(f"Invalid token type: expected {expected_type}")
    return payload


def get_token_expiration(token: str) -> datetime:
    """Extract expiration datetime from token."""
    payload = decode_token(token)
    exp = payload.get("exp")
    if not exp:
        raise UnauthorizedException("Token missing expiration")
    return datetime.fromtimestamp(exp, tz=timezone.utc)


def get_token_jti(token: str) -> str:
    """Extract unique JTI from token."""
    payload = decode_token(token)
    jti = payload.get("jti")
    if not jti:
        raise UnauthorizedException("Token missing JTI")
    return str(jti)
