from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from .datastore import IDataStore
from ...parser.base import IAST, IParser


class IPage(ABC):
    def __init__(self, datastore: IDataStore, path: Path):
        self._datastore = datastore
        self._path_to_page = path

    @abstractproperty
    def _content(self):
        pass

    def parse(self, parser: IParser) -> IAST:
        return parser.parse(self._content)
