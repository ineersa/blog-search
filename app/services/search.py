from langchain_chroma import Chroma
from components.retriever.VectorStoreRetriever import VectorStoreRetriever
from components.vectorstore import VectorStore
from .base import BaseService
from ..settings import SettingsLocal
from langchain_core.documents import Document as LangchainDocument


class SearchService(BaseService):

    def __init__(self,
                 collection: Chroma,
                 top_k: int = 5,
                 score_threshold: float = 0.2
                 ):
        super().__init__()
        self.collection: Chroma = collection
        self.vector_retriever = VectorStoreRetriever(collection=self.collection)
        self.vector_retriever.set_config(
            {
                "top_k": top_k,
                "score_threshold": score_threshold
            }
        )

    def search(self, query: str) -> list:
        documents = self.vector_retriever.retrieve(query=query)

        # Use a dictionary to keep track of unique IDs while preserving order
        id_dict = {}
        for document in documents:
            doc_id = document.metadata.get("id")
            if doc_id is not None and doc_id not in id_dict:
                id_dict[doc_id] = True

        # Convert the dictionary keys to a list to maintain order
        ids = list(id_dict.keys())

        return ids
