import zipfile
from pathlib import Path
from ..base import IDataStore


class NotionZipStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        return zipfile.Path(self._root, at=str(path)).exists()

    def read(self, path: Path) -> str:
        file_path = zipfile.Path(self._root) / path
        content = file_path.read_text()
        return content

    @property
    def name(self) -> str:
        return str(self._root)
