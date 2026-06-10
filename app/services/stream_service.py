import logging
from app.repositories.cache_interface import CacheRepository
from app.resolvers.resolver_interface import StreamResolver
from app.models import StreamInfo

logger = logging.getLogger(__name__)


class StreamService:

    def __init__(self, cache: CacheRepository, resolver: StreamResolver):
        self.cache = cache
        self.resolver = resolver

    def resolve(self, url: str) -> StreamInfo:
        cached = self.cache.get(url)

        if cached:
            logger.info("Cache hit for URL: %s", url)
            return cached

        logger.info("Cache miss for URL: %s. Resolving...", url)
        stream = self.resolver.resolve(url)

        self.cache.set(url, stream)
        logger.info("Resolved and cached URL: %s", url)

        return stream
