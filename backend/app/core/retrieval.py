from app.config import get_settings
from app.core.rag.embedder import embed_texts
from app.db.qdrant import get_qdrant_client

settings = get_settings()


async def retrieve(query: str, limit: int = 5):

    embedding = (await embed_texts([query]))[0]

    client = await get_qdrant_client()

    results = await client.query_points(
        collection_name=settings.qdrant_collection,
        query=embedding,
        limit=limit,
        with_payload=True,
    )

    output = []

    for point in results.points:

        payload = point.payload or {}

        output.append(
            {
                "text": payload.get("text", ""),
                "score": point.score,
                "metadata": {
                    "doc_id": payload.get("doc_id"),
                    "chunk_index": payload.get("chunk_index"),
                },
            }
        )

    return output