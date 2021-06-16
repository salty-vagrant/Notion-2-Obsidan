import zipfile
from pathlib import Path
from ..base import IDataStore, IPage
from .page import Page


class NotionZipStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        return zipfile.Path(self._root, at=str(path)).exists()

    def load_page(self, path: Path) -> IPage:
        return Page.from_datastore(self, path)

    @property
    def name(self) -> str:
        return str(self._root)
