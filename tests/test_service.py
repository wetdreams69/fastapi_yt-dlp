from app.services.stream_service import StreamService
from app.resolvers.resolver_interface import StreamResolver, StreamInfo


class DummyCache:
    def __init__(self):
        self.data = {}

    def get(self, key: str):
        return self.data.get(key)

    def set(self, key: str, value: object):
        self.data[key] = value


class DummyResolver(StreamResolver):
    def __init__(self):
        self.calls = 0

    def supports(self, url: str) -> bool:
        return True

    def resolve(self, url: str) -> StreamInfo:
        self.calls += 1
        return StreamInfo(
            title="Dummy",
            is_live=False,
            stream_url="http://url",
            format_id="best"
        )


def test_service_caching():
    cache = DummyCache()
    resolver = DummyResolver()
    service = StreamService(cache, resolver)

    res1 = service.resolve("http://url")
    res2 = service.resolve("http://url")

    assert res1 == res2
    assert resolver.calls == 1
