import logging
from typing import Dict

from components.interfaces import Reader
from components.postdocument import PostDocument
from app.database import SessionLocal, AutoBase
from app.schemas import PostsForRetrieval
from sqlalchemy import or_, and_


class BlogPostsReader(Reader):
    def __init__(self):
        super().__init__()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    def read(self) -> Dict[int, PostDocument]:
        documents = {}
        self.logger.info("Retrieving Blog Posts from DB")
        blog_posts = self.__read_posts_from_db()
        self.logger.info("Read {} Blog Posts from DB".format(len(blog_posts)))

        for item in blog_posts:
            document = PostDocument(
                doc_id=item.id,
                short_description=item.short_description,
                title=item.title,
                content=item.content,
            )
            documents[item.id] = document

        self.logger.info("Prepared {} documents".format(len(documents)))

        return documents

    def __read_posts_from_db(self) -> list[PostsForRetrieval]:
        with (SessionLocal() as db):
            table_class = AutoBase.classes['posts']
            blog_posts = db.query(
                AutoBase.classes['posts'].id,
                AutoBase.classes['posts'].title,
                AutoBase.classes['posts'].content,
                AutoBase.classes['posts'].short_description,
            ).where(
                or_(
                    table_class.processed_at == None,
                    table_class.processed_at < table_class.updated_at
                )
            ).all()

            blog_posts = [
                PostsForRetrieval(
                    id=item.id,
                    title=str(item.title),
                    content=str(item.content),
                    short_description=str(item.short_description)
                )
                for item in blog_posts
            ]

        return blog_posts
