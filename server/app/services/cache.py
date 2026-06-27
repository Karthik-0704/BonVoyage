import json
import os
import hashlib
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
DEFAULT_TTL = 3600  # 1 hour

_client = None


async def get_redis() -> aioredis.Redis:
    global _client
    if _client is None:
        _client = aioredis.from_url(REDIS_URL, decode_responses=True)
    return _client


def make_key(prefix: str, **kwargs) -> str:
    raw = json.dumps(kwargs, sort_keys=True)
    digest = hashlib.md5(raw.encode()).hexdigest()
    return f"{prefix}:{digest}"


async def cache_get(key: str):
    r = await get_redis()
    val = await r.get(key)
    return json.loads(val) if val else None


async def cache_set(key: str, value, ttl: int = DEFAULT_TTL):
    r = await get_redis()
    await r.set(key, json.dumps(value), ex=ttl)
