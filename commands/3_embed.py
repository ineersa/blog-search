import joblib
from langchain_core.documents import Document as LangchainDocument
from app.logger import get_logger
from app.settings import SettingsLocal
from components.vectorstore import VectorStore
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

logger = get_logger("commands/3_embed")


def run():
    langchain_docs: list[LangchainDocument] = joblib.load(SettingsLocal.DOCUMENTS_DUMP_FILE)
    # get ids of posts to update or add
    new_ids = set()
    for doc in langchain_docs:
        new_ids.add(doc.metadata["id"])

    #
    embedder = SentenceTransformerEmbeddings(
        model_name=SettingsLocal.TRANSFORMERS_MODEL,
        show_progress=True,
    )
    vector_store = VectorStore(embedder=embedder)
    collection: Chroma = vector_store.get_posts_collection()

    documents_to_delete = collection.get(where={"id": {"$in": list(new_ids)}})
    if len(documents_to_delete["ids"]) > 0:
        collection.delete(ids=documents_to_delete["ids"])

    collection.add_documents(langchain_docs)

    #d = collection.get(where={"id": 1}, include=["metadatas", "documents", "embeddings"])


if __name__ == '__main__':
    run()
