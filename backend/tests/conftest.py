import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture(autouse=True)
def disable_rate_limiter():
    with patch("fastapi_limiter.depends.RateLimiter.__call__", new_callable=AsyncMock) as mock:
        yield mock
