from typing import TYPE_CHECKING
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

    @abstractproperty
    def name(self) -> str:
        pass
