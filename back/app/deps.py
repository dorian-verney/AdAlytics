"""Shared dependencies (redis, cache, db session). No app/routes imports."""
import os
import redis

from .services import Services
from .my_redis.utils import CacheProxy
from .database.database import get_async_session

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

redis_cache = CacheProxy(
    services=Services,
    redis=r,
    methods_to_flush=["create_user", "delete_user", "update_user", "login"],
)

__all__ = ["redis_cache", "get_async_session", "r"]
