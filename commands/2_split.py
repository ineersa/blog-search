import joblib

from app.logger import get_logger
from app.settings import SettingsLocal
from components.reader.DiskDumpReader import DiskDumpReader
from components.loader.PostDocumentsLoader import PostDocumentsLoader

logger = get_logger("commands/2_split")


def run():
    logger.info("Loading data from disk")
    disk_dump_reader = DiskDumpReader()
    documents = disk_dump_reader.read()
    logger.info("Loading data from disk DONE")
    logger.info("generating documents for chunks")
    loader = PostDocumentsLoader(documents)
    langchain_docs = loader.load()
    logger.info("generating documents for chunks DONE")

    logger.info("dumping new documents to drive")
    joblib.dump(langchain_docs, SettingsLocal.DOCUMENTS_DUMP_FILE)
    logger.info("Finished")


if __name__ == '__main__':
    run()
