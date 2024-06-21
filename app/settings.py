import os.path
from . import ROOT_DIR, DATA_DIR
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath, FilePath


class Settings(BaseSettings):
    APP_NAME: str
    APP_DEBUG: bool
    LOG_LEVEL: int
    LOG_FILE: str
    DATABASE_URL: str
    DATA_DIR: DirectoryPath = DirectoryPath(DATA_DIR)
    ROOT_DIR: DirectoryPath = DirectoryPath(ROOT_DIR)
    DOCUMENTS_DUMP_FILE: str = os.path.join(DATA_DIR, 'documents.dump.gz')
    TRANSFORMERS_MODEL: str = "all-MiniLM-L6-v2"

    model_config = SettingsConfigDict(
        env_file=(
            os.path.join(ROOT_DIR, '.env'),
            os.path.join(ROOT_DIR, '.env.local'),
        ),
        env_file_encoding='utf-8',
        extra='ignore',
    )


SettingsLocal = Settings()
