import os

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from app.settings import SettingsLocal
from components.interfaces import Component


class VectorStore(Component):
    def __init__(self):
        super().__init__()
        self.config = {
            "posts_directory": os.path.join(SettingsLocal.DATA_DIR, "posts"),
            "embedder": SentenceTransformerEmbeddings(
                model_name=SettingsLocal.TRANSFORMERS_MODEL,
            )
        }

    def get_posts_collection(self) -> Chroma:
        return Chroma(
            collection_name="posts",
            embedding_function=self.config["embedder"],
            persist_directory=self.config["posts_directory"],
        )
