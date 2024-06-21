from langchain_core.documents import Document as LangchainDocument
from langchain_text_splitters import SentenceTransformersTokenTextSplitter

from app.settings import SettingsLocal
from components.interfaces import Splitter


class SentenceSplitter(Splitter):
    def __init__(self):
        super().__init__()
        self.config = {
            "model": SettingsLocal.TRANSFORMERS_MODEL,
            "overlap": 10,
            "tokens_per_chunk": 30,
        }
        self._splitter = None

    def setup(self):
        self._splitter = SentenceTransformersTokenTextSplitter(
            model_name=self.config["model"],
            chunk_overlap=self.config["overlap"],
            tokens_per_chunk=self.config["tokens_per_chunk"],
        )

    def split(self, text: str) -> list[LangchainDocument]:
        if self._splitter is None:
            raise Exception("First you need to initialise the splitter via setup()")
        docs = []
        texts = self._splitter.split_text(text)
        for text in texts:
            docs.append(LangchainDocument(page_content=text, metadata={}))

        return docs
