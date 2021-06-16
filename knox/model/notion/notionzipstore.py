from pathlib import Path
from ..base import IDataStore


class NotionZipStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        raise (NotImplementedError)

    def read(self, path: Path) -> str:
        raise (NotImplementedError)

    @property
    def name(self) -> str:
        return str(self._root)
