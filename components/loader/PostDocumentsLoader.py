from typing import Dict

from components.interfaces import Loader
from components.postdocument import PostDocument
from langchain_core.documents import Document as LangchainDocument
from components.splitter.MarkdownSplitter import MarkdownSplitter
from components.splitter.SentenceSplitter import SentenceSplitter


class PostDocumentsLoader(Loader):
    def __init__(self, post_documents: Dict[int, PostDocument]):
        super().__init__()

        self.post_documents = post_documents
        self.markdown_splitter = MarkdownSplitter()
        self.sentence_splitter = SentenceSplitter()
        self.sentence_splitter.setup()

    def load(self) -> Dict[str, LangchainDocument]:
        langchain_documents = []
        for doc_id, post_document in self.post_documents.items():
            if post_document.title_embedding is False:
                langchain_documents.append(LangchainDocument(
                    page_content=post_document.title,
                    metadata={"id": doc_id, "source": "title", "type": "title"},
                ))
            if post_document.short_description_embedding is False:
                docs = self.sentence_splitter.split(post_document.short_description)
                for doc in docs:
                    doc.metadata["source"] = "short_description"
                    doc.metadata["id"] = "doc_id"
                    doc.metadata["type"] = "text"
                    langchain_documents.append(doc)

            if post_document.content_embedding is False:
                docs = self.markdown_splitter.split(post_document.content)
                for doc in docs:
                    # if doc.metadata["type"] == "text":
                    sentences_docs = self.sentence_splitter.split(doc.page_content)
                    for sentence in sentences_docs:
                        sentence.metadata = doc.metadata
                        langchain_documents.append(sentence)
                    # else:
                    #     langchain_documents.append(doc)

        return langchain_documents