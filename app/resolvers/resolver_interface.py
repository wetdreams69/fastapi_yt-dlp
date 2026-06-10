from abc import ABC, abstractmethod
from app.models import StreamInfo


class ResolutionError(Exception):
    pass


class StreamResolver(ABC):

    @abstractmethod
    def resolve(self, url: str) -> StreamInfo:
        pass

    @abstractmethod
    def supports(self, url: str) -> bool:
        pass
