from typing import List
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from knox.renderer import Renderer
from .datastore import IDataStore
from .link import Link


class IPage(ABC):
    @classmethod
    @abstractmethod
    def from_datastore(cls, datastore: IDataStore, path: Path) -> "IPage":
        pass

    @classmethod
    @abstractmethod
    def create_renderer(cls, ext: str, config: dict = {}) -> Renderer:
        pass

    @abstractmethod
    def attach(self, datastore: IDataStore, path: Path):
        pass

    @abstractproperty
    def on_page_links(self) -> List[Link]:
        pass
