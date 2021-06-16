from ..base import IDataStore, IPage, BadDataStore
from pathlib import Path
from .notiondirstore import NotionDirStore
from .notionzipstore import NotionZipStore
from zipfile import ZipFile, BadZipFile
import logging

logger = logging.getLogger("__name__")


class Notion(IDataStore):
    _delegate: IDataStore

    def __init__(self, path: Path):
        if not path.exists():
            raise FileNotFoundError()

        if path.is_dir():
            self._delegate = NotionDirStore(path)
        elif self._isZip(path):
            self._delegate = NotionZipStore(path)
        else:
            raise BadDataStore(
                f"Attempt to open wrong type from Notion datastore: {path}"
            )

    def _isZip(self, path: Path) -> bool:
        try:
            with ZipFile(path, "r"):
                return True
        except (BadZipFile, FileNotFoundError):
            return False

    def exists(self, path: Path) -> bool:
        return self._delegate.exists(path)

    def load_page(self, path: Path) -> IPage:
        if not self.exists(path):
            raise FileNotFoundError(f"{path} not found in {self.name}")
        return self._delegate.load_page(path)

    @property
    def name(self) -> str:
        return self._delegate.name
