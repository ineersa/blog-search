import os
from typing import Dict

import joblib
from components.interfaces import Reader
from components.postdocument import PostDocument
from app.settings import SettingsLocal


class DiskDumpReader(Reader):
    def __init__(self):
        super().__init__()

    def read(self) -> Dict[int, PostDocument]:
        self.logger.info("Reading dumped file {}".format(SettingsLocal.DOCUMENTS_DUMP_FILE))

        if not os.path.exists(SettingsLocal.DOCUMENTS_DUMP_FILE):
            return {}

        documents = joblib.load(SettingsLocal.DOCUMENTS_DUMP_FILE)

        return documents
