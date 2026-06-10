from abc import ABC, abstractmethod


class CacheRepository(ABC):

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value: object):
        pass
