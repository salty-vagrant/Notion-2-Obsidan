from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from .datastore import IDataStore
from ...parser.base import IAST, IParser


class IPage(ABC):
    @classmethod
    @abstractmethod
    def from_datastore(cls, datastore: IDataStore, path: Path) -> "IPage":
        pass
