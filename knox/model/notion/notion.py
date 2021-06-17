from ..base import IDataStore, IPage, BadDataStore, BadPage
from pathlib import Path
from .notiondirstore import NotionDirStore
from .notionzipstore import NotionZipStore
from zipfile import ZipFile, BadZipFile
import logging

logger = logging.getLogger("__name__")

NOTION_PAGE_EXTENSIONS = [".md", ".csv"]


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

    def _is_page(self, path: Path) -> bool:
        return len(set(path.suffixes) & set(NOTION_PAGE_EXTENSIONS)) > 0

    def exists(self, path: Path) -> bool:
        return self._delegate.exists(path)

    def load_page(self, path: Path) -> IPage:
        if not self.exists(path):
            raise FileNotFoundError(f"{path} not found in {self.name}")
        if not self._is_page(path):
            raise BadPage(f"{path} is not recognised as a page resource in {self.name}")
        return self._delegate.load_page(path)

    @property
    def name(self) -> str:
        return self._delegate.name
