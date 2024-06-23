import logging
import sys
import datetime
import uvicorn
from fastapi import FastAPI
from langchain_community.embeddings import SentenceTransformerEmbeddings

from app.services.search import SearchService
from app.settings import SettingsLocal
from app.logger import get_logger
from components.vectorstore import VectorStore
from collections import OrderedDict

app = FastAPI(
    debug=SettingsLocal.APP_DEBUG,
    title=SettingsLocal.APP_NAME,
)

logger = get_logger(__name__)
embedder = SentenceTransformerEmbeddings(
    model_name=SettingsLocal.TRANSFORMERS_MODEL,
    show_progress=False,
)
vector_store = VectorStore(embedder=embedder)
posts_collection = vector_store.get_posts_collection()
posts_search_service = SearchService(collection=posts_collection)

@app.get("/")
async def root():
    return {
        "message": "Welcome to {}".format(SettingsLocal.APP_NAME),
        "time": datetime.datetime.now()
    }


@app.get("/search")
async def search(query: str):
    logger.info(f"Query is {query}")

    ids = posts_search_service.search(query=query)
    logger.info(f"Found {len(ids)} posts, ids {','.join(map(str, ids))}")
    return OrderedDict([
        ("ids", ids)
    ])

# just for development locally
if __name__ == '__main__':
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=3335,
        reload=True,
        workers=1,
        root_path="",
        proxy_headers=True,
        log_level=SettingsLocal.LOG_LEVEL
    )