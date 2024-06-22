import datetime

import joblib

from app.logger import get_logger
from components.reader.BlogPostsReader import BlogPostsReader
from app.settings import SettingsLocal
from app.database import SessionLocal, AutoBase


logger = get_logger("commands/1_read")

def run():
    blog_posts_reader = BlogPostsReader()
    documents = blog_posts_reader.read()
    logger.info("Done reading blog_posts data")

    logger.info("Dumping to drive")
    joblib.dump(documents, SettingsLocal.POST_DOCUMENTS_DUMP_FILE)

    # Update records in database set processed_at
    logger.info("updating records")
    with SessionLocal() as db:
        total_updated = 0
        for id, document in documents.items():
            result = db.execute(
                AutoBase.metadata.tables['posts'].update()
                .where(AutoBase.metadata.tables['posts'].c.id == id)
                .values(processed_at=datetime.datetime.now())
            )
            total_updated += result.rowcount

        # Explicitly commit the transaction
        db.commit()
        logger.info(f"Update completed. Total rows updated: {total_updated}")

    logger.info("Finished")


if __name__ == '__main__':
    run()