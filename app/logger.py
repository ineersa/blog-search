import logging
from app.settings import SettingsLocal

logging.basicConfig(
    level=SettingsLocal.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s @ %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if SettingsLocal.LOG_FILE:
        handler = logging.FileHandler(SettingsLocal.LOG_FILE)
        logger.addHandler(handler)

    return logger
