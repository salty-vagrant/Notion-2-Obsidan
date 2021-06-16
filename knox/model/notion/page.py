from ..base import IPage, IDataStore
from pathlib import Path


class Page(IPage):
    @classmethod
    def from_datastore(cls, datastore: IDataStore, path: Path, attach=False) -> "Page":
        if not datastore.exists(path):
            raise FileNotFoundError(f"Could not load {path} from {datastore.name}")
        new_page = cls()
        if attach:
            new_page.attach(datastore, path)
        return new_page

    def attach(self, datastore: IDataStore, path: Path):
        if not datastore.exists(path):
            raise FileNotFoundError(
                f"Could not attach Page to  {path} in {datastore.name}"
            )
        self._datastore = datastore
        self._path = path
