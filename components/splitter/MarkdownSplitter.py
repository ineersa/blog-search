import io
import os

from components.chunk import Chunk
from components.interfaces import Splitter
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from app.settings import SettingsLocal
from components.loader.UnstructuredMarkdownFileIOLoader import UnstructuredMarkdownFileIOLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter

class MarkdownSplitter(Splitter):

    def __init__(self):
        super().__init__()
        self.__splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN, chunk_size=100, chunk_overlap=0
        )

    def split(self, text: str) -> list[Chunk]:
        file_like_object = io.StringIO(text)
        loader = UnstructuredMarkdownFileIOLoader(file=file_like_object, mode="single")
        documents = loader.load()

        sentence_splitter = SentenceTransformersTokenTextSplitter(
            model_name=SettingsLocal.TRANSFORMERS_MODEL
        )


        loader2 = UnstructuredMarkdownLoader(os.path.join(SettingsLocal.DATA_DIR, "test.md"), mode="elements")
        documents2 = loader2.load()
        docs = self.__splitter.create_documents([text])

        print(321)

        return list()