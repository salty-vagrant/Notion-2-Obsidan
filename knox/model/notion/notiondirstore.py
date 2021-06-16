from pathlib import Path
from ..base import IDataStore, IPage
from .page import Page
import logging

logger = logging.getLogger("__name__")


class NotionDirStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        ds_path = self._root / path
        return ds_path.exists()

    def load_page(self, path: Path) -> IPage:
        return Page.from_datastore(self, path)

    @property
    def name(self) -> str:
        return str(self._root)
