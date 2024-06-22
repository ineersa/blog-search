# Simple blog search system

Purpose of this project to play around with modern RAG libraries and create retrieval system for my blog.

# Disclaimer
This code is not recommended for usage to anyone.
If you want - you can pick some parts from it, or check in learning purposes.

## Commands
Why commands have so strange names? 

Well they are done in order, to emulate pipeline.

For convenience, we store intermediate results in files using joblib.

## System components

### Readers
 - `BlogPostsReader` reads data from database and creates `PostDocument`'s
 - `DiskDumpReader` reads dumped data from disk with `PostDocument`'s

### Loaders
 - `PostDoumentsLoader` loads data from `PostDocument`'s into Langchain `Document`s, this also includes splitting our documents

### Splitters
 - `MarkdownSplitter` splits text into Langchain `Document`s, I've had to write own because strangely markdown splitters from Langchain, Unstructured and LlamaIndex all failed to make correct splits and identify code blocks, which is very strange.
 - `SentenceSplitter` wrapper on `SentenceTransformersTokenTextSplitter` to make it compatible with interface and easy usage

### Embedders
I'm using `sentence-transformers` library with `all-MiniLM-L6-v2` model because it's small and fast.
That's why I used in vector store one provided from 
```python
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from app.settings import SettingsLocal
from components.interfaces import Component


class VectorStore(Component):
    def __init__(self):
        super().__init__()
        self.config = {
            "posts_directory": os.path.join(SettingsLocal.DATA_DIR, "posts"),
            "embedder": SentenceTransformerEmbeddings(
                model_name=SettingsLocal.TRANSFORMERS_MODEL,
            )
        }
```
And you can implement `langchain_core.embeddings.embeddings.Embeddings` interface and add your own embedder to components.
You can easily add it to vector store via config dict.

### Retrievers
