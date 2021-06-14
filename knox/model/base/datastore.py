from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path


class IDataStore(ABC):
    def __init__(self, source: Path):
        if not source.exists():
            raise FileNotFoundError()
        self._root = source
