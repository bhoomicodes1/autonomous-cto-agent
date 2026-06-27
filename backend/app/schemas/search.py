from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str


class SearchResult(BaseModel):
    text: str
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    results: list[SearchResult]