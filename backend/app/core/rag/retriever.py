from qdrant_client.http.models import (
    Filter,
    FieldCondition,
    MatchValue,
)

from app.config import get_settings
from app.core.rag.embedder import embed_texts
from app.db.qdrant import get_qdrant_client

settings = get_settings()


async def retrieve(
    query: str,
    owner: str,
    repo: str,
    limit: int = 10,
):
    """
    Retrieve the most relevant repository chunks from Qdrant.
    """

    embedding = (await embed_texts([query]))[0]

    client = await get_qdrant_client()

    results = await client.query_points(
        collection_name=settings.qdrant_collection,
        query=embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="owner",
                    match=MatchValue(value=owner),
                ),
                FieldCondition(
                    key="repo",
                    match=MatchValue(value=repo),
                ),
            ]
        ),
        limit=limit,
        with_payload=True,
    )

    output = []

    for point in results.points:

        # Ignore weak matches
        if point.score < 0.60:
            continue

        payload = point.payload or {}

        text = payload.get("text", "")

        # -----------------------------
        # Skip implementation-heavy chunks
        # -----------------------------

        if len(text) > 1800:
            continue

        if text.count("def ") >= 3:
            continue

        if text.count("class ") >= 2:
            continue

        if text.count("import ") >= 8:
            continue

        if text.count("{") > 20:
            continue

        if text.count("}") > 20:
            continue

        if text.count("(") > 60:
            continue

        output.append(
            {
                "text": text,
                "score": point.score,
                "doc_id": payload.get("doc_id"),
                "chunk_index": payload.get("chunk_index"),
                "file": payload.get("doc_id"),
            }
        )

    output.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    print("\n========== RETRIEVED CHUNKS ==========")

    for item in output:
        print(
            f"{item['score']:.3f} | {item['file']}"
        )

    print("======================================\n")

    return output