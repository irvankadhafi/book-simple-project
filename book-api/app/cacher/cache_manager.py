import json
from redis import Redis
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class CacheManager:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def get(self, key: str) -> Optional[str]:
        return self.redis.get(key)

    def set(self, key: str, value: str, expire: int = None):
        if expire:
            self.redis.setex(key, expire, value)
        else:
            self.redis.set(key, value)

    def delete(self, key: str):
        self.redis.delete(key)

    def delete_many(self, keys: list[str]):
        self.redis.delete(*keys)

class CacheItem(Generic[T]):
    def __init__(self, key: str, value: T):
        self.key = key
        self.value = value

def new_cache_item(key: str, value: T) -> CacheItem[T]:
    return CacheItem(key, json.dumps(value))

def find_from_cache_by_key(cache: CacheManager, key: str) -> Optional[str]:
    return cache.get(key)
