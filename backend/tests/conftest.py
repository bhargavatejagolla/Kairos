import pytest
from unittest.mock import patch
from fastapi import Request, Response

async def mock_rate_limiter_call(self, request: Request, response: Response, pydantic_schema=None):
    pass

from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

@pytest.fixture(autouse=True)
def init_cache_and_disable_limiter():
    # Initialize cache for tests
    FastAPICache.init(InMemoryBackend())
    
    # Disable rate limiter
    with patch("fastapi_limiter.depends.RateLimiter.__call__", new=mock_rate_limiter_call):
        yield

