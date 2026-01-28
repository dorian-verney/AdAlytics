import json
from sqlalchemy.ext.asyncio import AsyncSession


def _serialize_for_cache(val):
    """JSON-serializable form for cache (e.g. list[UserOut] -> list[dict])."""
    if isinstance(val, list) and val and hasattr(val[0], "model_dump"):
        return [x.model_dump() for x in val]
    if hasattr(val, "model_dump"):
        return val.model_dump()
    return val

class CacheProxy:
    def __init__(
        self,
        services,
        redis,
        methods_to_flush=[]
    ):
        self._redis = redis
        self._methods_to_flush = methods_to_flush
        self._services = services

    def __getattr__(self, method_name):
        method = getattr(self._services, method_name)

        if not callable(method):
            return method

        async def wrapper(*args, **kwargs):
            if method_name in self._methods_to_flush:
                self._redis.flushdb()
                return await method(*args, **kwargs)

            # need to remove the session from the args
            # we suppose that the `session` argument is the last argument
            args_cache = args[:-1] if len(args) > 0 and isinstance(args[-1], AsyncSession) else args
            cache_key = f"{method_name}-{json.dumps(args_cache, sort_keys=True)}"
            cached = self._redis.get(cache_key)
            if cached is not None and cached != "":
                # CACHE HIT - returning from cache (no DB)
                return json.loads(cached)

            # CACHE MISS - executing method and caching result
            result = await method(*args, **kwargs)
            to_cache = _serialize_for_cache(result)
            self._redis.set(cache_key, json.dumps(to_cache, default=str))
            return to_cache

        return wrapper


