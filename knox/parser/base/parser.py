from abc import ABC, abstractmethod
from .ast import IAST


class IParser(ABC):
    @abstractmethod
    def parse(self, content: str) -> IAST:
        pass
