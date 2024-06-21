import joblib

from app.logger import get_logger
from components.reader.DiskDumpReader import DiskDumpReader
from components.splitter.MarkdownSplitter import MarkdownSplitter

def run():
    disk_dump_reader = DiskDumpReader()
    documents = disk_dump_reader.read()
    splitter = MarkdownSplitter()

    for id, document in documents.items():
        if len(document.chunks) == 0:
            chunks = splitter.split(document.content)

        print(123)


if __name__ == '__main__':
    run()