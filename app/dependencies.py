from fastapi import Depends
from app.config import get_settings
from app.repositories.memory_cache import MemoryCache
from app.repositories.cache_interface import CacheRepository
from app.resolvers.youtube_resolver import YoutubeResolver
from app.resolvers.twitch_resolver import TwitchResolver
from app.resolvers.pluto_resolver import PlutoResolver
from app.resolvers.routing_resolver import RoutingResolver
from app.resolvers.resolver_interface import StreamResolver
from app.services.stream_service import StreamService

_settings = get_settings()
_cache = MemoryCache(ttl_seconds=_settings.cache_ttl)
_resolver = RoutingResolver([
    YoutubeResolver(cookies_file=_settings.cookies_file),
    TwitchResolver(cookies_file=_settings.cookies_file),
    PlutoResolver(cookies_file=_settings.cookies_file),
])


def get_cache() -> CacheRepository:
    return _cache


def get_resolver() -> StreamResolver:
    return _resolver


def get_stream_service(
    cache: CacheRepository = Depends(get_cache),
    resolver: StreamResolver = Depends(get_resolver)
) -> StreamService:
    return StreamService(cache, resolver)
