from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path


class IDataStore(ABC):
    @abstractmethod
    def exists(self, path: Path) -> bool:
        pass

    @abstractmethod
    def read(self, path: Path) -> str:
        pass

    @abstractproperty
    def name(self) -> str:
        pass
