from contextlib import contextmanager

import redis

from app.core.config import settings

# Shared Redis client for background platform
redis_client = redis.from_url(settings.redis_url, decode_responses=True)

class DistributedLockError(Exception):
    pass

@contextmanager
def distributed_lock(lock_key: str, timeout: int = 60, blocking_timeout: int = 5):
    """
    Acquires a Redis lock for idempotency.
    Throws DistributedLockError if unable to acquire.
    """
    lock = redis_client.lock(
        name=f"kairos:lock:{lock_key}",
        timeout=timeout,
        blocking_timeout=blocking_timeout
    )
    acquired = lock.acquire()
    if not acquired:
        raise DistributedLockError(f"Could not acquire lock for {lock_key}")
    
    try:
        yield lock
    finally:
        try:
            lock.release()
        except redis.exceptions.LockError:
            pass # Lock already released or expired
