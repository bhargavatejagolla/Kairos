import time
from .distributed_lock import redis_client

class RateLimitExceeded(Exception):
    pass

class RateLimiter:
    """
    Redis-backed token bucket or simple counter for rate limiting.
    """
    @staticmethod
    def check_limit(key: str, max_requests: int, window_seconds: int = 60):
        """
        Simple sliding window / fixed window using Redis INCR & EXPIRE.
        """
        redis_key = f"kairos:ratelimit:{key}:{int(time.time() / window_seconds)}"
        
        current = redis_client.incr(redis_key)
        if current == 1:
            redis_client.expire(redis_key, window_seconds)
            
        if current > max_requests:
            raise RateLimitExceeded(f"Rate limit exceeded for {key}")
        
        return True
