from typing import List
import zipfile
from pathlib import Path
from ..base import IDataStore, IPage, BadPage
from .page import Page


class NotionZipStore(IDataStore):
    def __init__(self, path: Path):
        self._root = path

    def exists(self, path: Path) -> bool:
        return zipfile.Path(self._root, at=str(path)).exists()

    def load_page(self, path: Path) -> IPage:
        return Page.from_datastore(self, path)

    def new_page(self, path: Path) -> IPage:
        if self.exists(path):
            raise BadPage(f"{path} already exists in {self.name}")
        page = Page()
        with zipfile.ZipFile(self._root, "a") as zfile:
            zfile.writestr(str(path), b"")
        page.attach(self, path)
        return page

    def read_resource(self, path: Path) -> bytes:
        with zipfile.ZipFile(self._root, "r") as zfile:
            content = zfile.read(str(path))
        return content

    @property
    def name(self) -> str:
        return str(self._root)

    @property
    def resources(self) -> List[str]:
        with zipfile.ZipFile(self._root, "r") as zfile:
            result = [f.rstrip("/") for f in zfile.namelist()]
        return result
