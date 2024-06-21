class Chunk:
    def __init__(
        self,
        doc_id: int,
        chunk_id: int,
        text: str,
    ):
        self.text = text
        self.doc_id = doc_id
        self.chunk_id = chunk_id
        self.embedding = False