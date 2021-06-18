from typing import List
from pathlib import Path
from ..base import IDataStore, IPage, BadPage
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

    def new_page(self, path: Path) -> IPage:
        if self.exists(path):
            raise BadPage(f"{path} already exists in {self.name}")
        page = Page()
        page_path_on_disk = self._root / path
        page_path_on_disk.touch(exist_ok=False)
        page.attach(self, path)
        return page

    @property
    def name(self) -> str:
        return str(self._root)

    @property
    def resources(self) -> List[str]:
        return [str(f)[len(str(self._root)) + 1 :] for f in Path(self._root).rglob("*")]
