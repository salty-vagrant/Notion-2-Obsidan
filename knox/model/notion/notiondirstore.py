from pathlib import Path
from ..base import IDataStore
import logging

logger = logging.getLogger("__name__")


class NotionDirStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        ds_path = self._root / path
        return ds_path.exists()

    def read(self, path: Path) -> str:
        file_path = self._root / path
        with open(file_path, "r") as f:
            content = f.read()
        return content

    @property
    def name(self) -> str:
        return str(self._root)
