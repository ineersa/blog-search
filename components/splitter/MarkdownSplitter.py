import re

from components.interfaces import Splitter
from langchain_core.documents import Document as LangchainDocument


class MarkdownSplitter(Splitter):

    def __init__(self):
        super().__init__()

    def split(self, text: str) -> list[LangchainDocument]:
        # Add a newline at the beginning and end to ensure the first header is captured
        text = '\n' + text + '\n'

        # Split the content into sections based on headers
        sections = re.split(r'\n(#+\s.*)\n', text)

        # Handle case where there are no headers
        if len(sections) == 1:
            sections = ["", "# Root", sections[0]]

        documents = []
        for i in range(1, len(sections), 2):
            header = sections[i].strip()
            header_text = re.sub(r'^#+\s*', '', header).strip()
            content = sections[i + 1].strip() if i + 1 < len(sections) else ""

            # if it's our generated root, skip
            if header_text != "Root":
                # Add the header as a separate document
                documents.append(LangchainDocument(
                    page_content=header_text,
                    metadata={
                        "type": "title",
                        "level": header.count('#'),
                    }
                ))

            # Split content into paragraphs and code blocks
            parts = re.split(r'(```[\s\S]*?```)', content)

            for part in parts:
                if part.strip():
                    if part.startswith('```') and part.endswith('```'):
                        # This is a code block
                        language = part.split('\n')[0][3:].strip()
                        code = '\n'.join(part.split('\n')[1:-1])
                        doc = LangchainDocument(
                            page_content=code,
                            metadata={
                                "type": "code",
                                "language": language,
                                "header": header,
                            }
                        )
                    else:
                        # This is regular text
                        # Replace newlines with spaces, except for double newlines (paragraphs)
                        text = re.sub(r'(?<!\n)\n(?!\n)', ' ', part.strip())
                        text = re.sub(r'\n{2,}', '\n', text)
                        doc = LangchainDocument(
                            page_content=text,
                            metadata={
                                "type": "text",
                                "header": header,
                            }
                        )
                    documents.append(doc)

        return documents
