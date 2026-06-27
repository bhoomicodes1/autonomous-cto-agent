from fastapi import APIRouter

from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.core.retrieval import retrieve

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post("/", response_model=SearchResponse)
async def search(request: SearchRequest):

    results = await retrieve(request.query)

    return SearchResponse(
        results=[
            SearchResult(
                text=r["text"],
                score=r["score"],
                metadata=r["metadata"],
            )
            for r in results
        ]
    )