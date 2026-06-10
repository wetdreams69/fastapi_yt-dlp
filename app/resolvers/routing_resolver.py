from app.models import StreamInfo
from app.resolvers.resolver_interface import StreamResolver, ResolutionError


class RoutingResolver(StreamResolver):

    def __init__(self, resolvers: list[StreamResolver]):
        self.resolvers = resolvers

    def supports(self, url: str) -> bool:
        return any(r.supports(url) for r in self.resolvers)

    def resolve(self, url: str) -> StreamInfo:
        for r in self.resolvers:
            if r.supports(url):
                return r.resolve(url)
        raise ResolutionError("Unsupported platform or URL")
