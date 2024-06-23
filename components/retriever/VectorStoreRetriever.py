from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.documents import Document as LangchainDocument

from app.settings import SettingsLocal
from components.interfaces import Retriever
from components.vectorstore import VectorStore
from langchain_chroma import Chroma

class VectorStoreRetriever(Retriever):
    def __init__(self, collection: Chroma):
        super().__init__()
        self.collection = collection

        self.config = {
            "top_k": 5,
            "score_threshold": 0.1
        }

    def retrieve(self, query: str) -> list[LangchainDocument]:
        documents_with_scores = self.collection.similarity_search_with_relevance_scores(
            query=query,
            k=self.config["top_k"],
            score_threshold=self.config["score_threshold"],
        )
        documents = [doc for doc, score in documents_with_scores]

        return documents
