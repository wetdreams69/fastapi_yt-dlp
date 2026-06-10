from time import time
from app.repositories.cache_interface import CacheRepository


class MemoryCache(CacheRepository):

    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self.storage = {}

    def _cleanup(self):
        now = time()
        expired = [k for k, v in self.storage.items() if v["expires_at"] < now]
        for k in expired:
            del self.storage[k]

    def get(self, key: str):
        item = self.storage.get(key)

        if not item:
            return None

        if item["expires_at"] < time():
            del self.storage[key]
            return None

        return item["value"]

    def set(self, key: str, value: object):
        self._cleanup()
        self.storage[key] = {
            "value": value,
            "expires_at": time() + self.ttl_seconds,
        }
