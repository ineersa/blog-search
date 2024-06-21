from components.chunk import Chunk
from components.postdocument import PostDocument
from app.logger import get_logger
from typing import Dict


class Component:

    def __init__(self):
        self.config = {}
        self.name = self.__class__.__name__
        self.logger = get_logger(self.__class__.__name__)

    def set_config(self, new_config: dict):
        for _k in new_config:
            if _k in self.config:
                self.config[_k] = new_config[_k]


class Reader(Component):

    def __init__(self):
        super().__init__()

    def read(self) -> Dict[int, PostDocument]:
        """
        :return: Dict[str, Document] map of documents, mapped by id
        """
        raise NotImplementedError("read method must be implemented by a subclass.")


class Splitter(Component):

    def __init__(self):
        super().__init__()

    def split(self, text: str) -> list[Chunk]:
        raise NotImplementedError("split method must be implemented by a subclass.")
