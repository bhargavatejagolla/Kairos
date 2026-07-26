from fastapi import Header, HTTPException, status
from typing import Optional

def get_idempotency_key(
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key", description="Idempotency key for safe retries")
) -> Optional[str]:
    # In a real enterprise system, you would check Redis or the DB to see if this key was already processed.
    # If processed, return the cached response.
    # For now, we simply extract the key and make it available to the workflow/command bus.
    return idempotency_key

def get_if_match(
    if_match: Optional[str] = Header(None, alias="If-Match", description="Optimistic locking ETag")
) -> Optional[str]:
    return if_match

def get_if_none_match(
    if_none_match: Optional[str] = Header(None, alias="If-None-Match", description="Browser caching ETag")
) -> Optional[str]:
    return if_none_match
