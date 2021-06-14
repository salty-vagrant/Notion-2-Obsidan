from abc import ABC, abstractmethod


class IPage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass
