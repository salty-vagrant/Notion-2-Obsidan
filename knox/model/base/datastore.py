from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path


class IDataStore(ABC):
    @abstractmethod
    def exists(self, path: Path) -> bool:
        pass
