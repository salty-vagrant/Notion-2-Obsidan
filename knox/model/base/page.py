from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from .datastore import IDataStore
from ...parser.base import IAST, IParser


class IPage(ABC):
    def __init__(self, datastore: IDataStore, path: Path):
        self._datastore = datastore
        self._path_to_page = path

    @property
    def exists(self) -> bool:
        return self._datastore.exists(self._path_to_page)
