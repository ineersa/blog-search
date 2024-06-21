import joblib

from app.logger import get_logger
from components.reader.BlogPostsReader import BlogPostsReader
from app.settings import SettingsLocal
from components.reader.DiskDumpReader import DiskDumpReader

logger = get_logger("commands/1_read")

def run():
    blog_posts_reader = BlogPostsReader()
    disk_dump_reader = DiskDumpReader()
    new_documents = blog_posts_reader.read()
    logger.info("Done reading blog_posts data")
    documents = disk_dump_reader.read()

    for id, document in new_documents.items():
        if id not in documents:
            logger.info("Adding document id={}".format(id))
            documents[id] = document
        else:
            logger.info("Refreshing document id={}".format(id))
            documents[id].refresh(document)

    logger.info("Dumping to drive")
    joblib.dump(new_documents, SettingsLocal.POST_DOCUMENTS_DUMP_FILE)
    logger.info("Finished")


if __name__ == '__main__':
    run()