from datetime import timedelta
from uuid import uuid4

import pytest

from app.core.exceptions import UnauthorizedException
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_token,
)


def test_create_and_decode_access_token() -> None:
    sub = str(uuid4())
    token = create_access_token(subject=sub)
    payload = decode_token(token)
    assert payload["sub"] == sub
    assert payload["type"] == "access"
    assert "exp" in payload


def test_create_and_verify_refresh_token() -> None:
    sub = str(uuid4())
    token = create_refresh_token(subject=sub)
    payload = verify_token(token, expected_type="refresh")
    assert payload["sub"] == sub
    assert payload["type"] == "refresh"


def test_verify_token_wrong_type() -> None:
    token = create_access_token(subject="123")
    with pytest.raises(UnauthorizedException, match="Invalid token type"):
        verify_token(token, expected_type="refresh")


def test_decode_expired_token() -> None:
    token = create_access_token(subject="123", expires_delta=timedelta(seconds=-1))
    with pytest.raises(UnauthorizedException, match="Token has expired"):
        decode_token(token)


def test_decode_invalid_token() -> None:
    with pytest.raises(UnauthorizedException, match="Invalid token"):
        decode_token("invalid.token.string")
