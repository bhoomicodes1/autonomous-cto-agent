from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    owner: str
    repo: str


class Source(BaseModel):
    text: str
    score: float
    doc_id: str
    chunk_index: int


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]