import os

from langchain_chroma import Chroma
from chromadb.config import Settings as ChromaSettings
from langchain_community.embeddings import SentenceTransformerEmbeddings
from app.settings import SettingsLocal
from components.interfaces import Component


class VectorStore(Component):
    def __init__(self, embedder: SentenceTransformerEmbeddings):
        super().__init__()
        self.config = {
            "posts_directory": os.path.join(SettingsLocal.DATA_DIR, "posts"),
        }
        self.embedder = embedder

    def get_posts_collection(self) -> Chroma:
        return Chroma(
            collection_name="posts",
            embedding_function=self.embedder,
            client_settings=ChromaSettings(
                anonymized_telemetry=False,
                is_persistent=True,
                persist_directory=self.config["posts_directory"]
            )
        )
