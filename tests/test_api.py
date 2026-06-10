import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_resolver
from app.resolvers.resolver_interface import StreamResolver, ResolutionError, StreamInfo

client = TestClient(app)


class MockResolver(StreamResolver):
    def supports(self, url: str) -> bool:
        return "mock" in url

    def resolve(self, url: str) -> StreamInfo:
        if "fail" in url:
            raise ResolutionError("Failed resolving")
        return StreamInfo(
            title="Mock Video",
            is_live=False,
            stream_url="http://mock-stream",
            format_id="123"
        )


@pytest.fixture(autouse=True)
def override_resolver():
    app.dependency_overrides[get_resolver] = lambda: MockResolver()
    yield
    app.dependency_overrides.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_resolve_endpoint_success():
    response = client.get("/resolve?url=http://mock", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://mock-stream"


def test_resolve_endpoint_failure():
    response = client.get("/resolve?url=http://mock-fail")
    assert response.status_code == 400
    assert response.json()["detail"] == "Failed resolving"
