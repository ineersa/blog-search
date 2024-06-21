from components.chunk import Chunk
from langchain_core.documents import Document as LangchainDocument

class PostDocument:
    def __init__(
            self,
            doc_id: int,
            title: str = "",
            short_description: str = "",
            content: str = ""
    ):
        self.doc_id = doc_id
        self.title = title
        self.short_description = short_description
        self.content = content
        self.title_embedding = False
        self.short_description_embedding = False
        self.chunks: list[Chunk] = []

    def refresh(self, new_doc: 'PostDocument'):
        if new_doc.title != self.title:
            self.title = new_doc.title
            self.title_embedding = False
        if new_doc.short_description != self.short_description:
            self.short_description = new_doc.short_description
            self.short_description_embedding = False
        if new_doc.content != self.content:
            self.content = new_doc.content
            self.chunks = []

    def to_langchain_documents(self) -> list[LangchainDocument]:
        langchain_documents = [LangchainDocument(
            page_content=self.title,
            metadata={"id": self.doc_id, "source": "title"},
        ), LangchainDocument(
            page_content=self.short_description,
            metadata={"id": self.doc_id, "source": "short_description"},
        )]

        for chunk in self.chunks:
            langchain_documents.append(
                LangchainDocument(
                    page_content=chunk.text,
                    metadata={"id": self.doc_id, "source": "chunk", "chunk_id": chunk.chunk_id},
                )
            )

        return langchain_documents
