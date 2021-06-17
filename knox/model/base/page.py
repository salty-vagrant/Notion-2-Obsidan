from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from .datastore import IDataStore


class IPage(ABC):
    @classmethod
    @abstractmethod
    def from_datastore(cls, datastore: IDataStore, path: Path) -> "IPage":
        pass

    @abstractmethod
    def attach(self, datastore: IDataStore, path: Path):
        pass
