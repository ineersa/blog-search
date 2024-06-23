from app.logger import get_logger


class BaseService:
    def __init__(self):
        self.name = self.__class__.__name__
        self.logger = get_logger(self.__class__.__name__)
