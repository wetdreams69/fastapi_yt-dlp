import pytest
from app.resolvers.resolver_interface import ResolutionError, StreamInfo
from app.resolvers.youtube_resolver import YoutubeResolver
from app.resolvers.twitch_resolver import TwitchResolver
from app.resolvers.pluto_resolver import PlutoResolver
from app.resolvers.routing_resolver import RoutingResolver


def test_provider_supports():
    yt = YoutubeResolver()
    tw = TwitchResolver()
    pl = PlutoResolver()

    assert yt.supports("https://www.youtube.com/watch?v=123")
    assert yt.supports("https://youtu.be/123")
    assert not yt.supports("https://twitch.tv/abc")

    assert tw.supports("https://twitch.tv/abc")
    assert not tw.supports("https://youtube.com/watch?v=123")

    assert pl.supports("https://pluto.tv/stream")
    assert not pl.supports("https://youtube.com/watch?v=123")


def test_routing_resolver_success():
    class DummyResolver:
        def supports(self, url: str) -> bool:
            return "dummy" in url

        def resolve(self, url: str) -> StreamInfo:
            return StreamInfo(
                title="Dummy",
                is_live=False,
                stream_url="http://dummy",
                format_id="best"
            )

    router = RoutingResolver([DummyResolver()])
    assert router.supports("http://dummy")
    res = router.resolve("http://dummy")
    assert res.title == "Dummy"


def test_routing_resolver_failure():
    router = RoutingResolver([])
    with pytest.raises(ResolutionError):
        router.resolve("http://any")
