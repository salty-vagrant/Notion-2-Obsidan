from typing import TYPE_CHECKING, List
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path

if TYPE_CHECKING:
    from .page import IPage


class IDataStore(ABC):
    @abstractmethod
    def exists(self, path: Path) -> bool:
        pass

    @abstractmethod
    def load_page(self, path: Path) -> "IPage":
        pass

    @abstractmethod
    def new_page(self, path: Path) -> "IPage":
        pass

    @abstractmethod
    def read_resource(self, path: Path) -> bytes:
        pass

    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def resources(self) -> List[str]:
        pass
