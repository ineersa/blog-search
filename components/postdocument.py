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
        self.content_embedding = False

    def refresh(self, new_doc: 'PostDocument'):
        if new_doc.title != self.title:
            self.title = new_doc.title
            self.title_embedding = False
        if new_doc.short_description != self.short_description:
            self.short_description = new_doc.short_description
            self.short_description_embedding = False
        if new_doc.content != self.content:
            self.content = new_doc.content
            self.content_embedding = False
