
from fastapi import Header


def get_idempotency_key(
    idempotency_key: str | None = Header(None, alias="Idempotency-Key", description="Idempotency key for safe retries")
) -> str | None:
    # In a real enterprise system, you would check Redis or the DB to see if this key was already processed.
    # If processed, return the cached response.
    # For now, we simply extract the key and make it available to the workflow/command bus.
    return idempotency_key

def get_if_match(
    if_match: str | None = Header(None, alias="If-Match", description="Optimistic locking ETag")
) -> str | None:
    return if_match

def get_if_none_match(
    if_none_match: str | None = Header(None, alias="If-None-Match", description="Browser caching ETag")
) -> str | None:
    return if_none_match
