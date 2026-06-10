import time
from app.repositories.memory_cache import MemoryCache


def test_cache_set_get():
    cache = MemoryCache(ttl_seconds=2)
    cache.set("key1", "val1")
    assert cache.get("key1") == "val1"


def test_cache_expiration():
    cache = MemoryCache(ttl_seconds=1)
    cache.set("key1", "val1")
    time.sleep(1.1)
    assert cache.get("key1") is None


def test_cache_cleanup():
    cache = MemoryCache(ttl_seconds=1)
    cache.set("key1", "val1")
    time.sleep(1.1)
    cache.set("key2", "val2")
    assert "key1" not in cache.storage
    assert "key2" in cache.storage
