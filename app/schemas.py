from pydantic import BaseModel


class PostsForRetrieval(BaseModel):
    id: int
    title: str
    short_description: str
    content: str