import joblib
from langchain_core.documents import Document as LangchainDocument
from app.logger import get_logger
from app.settings import SettingsLocal
from components.retriever.VectorStoreRetriever import VectorStoreRetriever
from components.vectorstore import VectorStore
from langchain_chroma import Chroma
from chromadb.config import Settings
from langchain_community.embeddings import SentenceTransformerEmbeddings

logger = get_logger("commands/4_retrieve")


def run():
    embedder = SentenceTransformerEmbeddings(
        model_name=SettingsLocal.TRANSFORMERS_MODEL,
        show_progress=True,
    )
    vector_store = VectorStore(embedder=embedder)
    collection: Chroma = vector_store.get_posts_collection()
    vector_retriever = VectorStoreRetriever(collection=collection)
    documents = vector_retriever.retrieve("PHP upgrade")

    print(documents)


if __name__ == '__main__':
    run()
