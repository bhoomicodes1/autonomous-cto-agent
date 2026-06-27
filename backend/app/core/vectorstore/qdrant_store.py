from uuid import uuid4

from qdrant_client.http.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from app.config import get_settings
from app.db.qdrant import get_qdrant_client

settings = get_settings()

COLLECTION_NAME = "architecture_docs"


async def create_collection():
    client = await get_qdrant_client()

    collections = await client.get_collections()

    names = [
        collection.name
        for collection in collections.collections
    ]

    if COLLECTION_NAME not in names:

        await client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        print("✅ Qdrant Collection Created")

    else:
        print("✅ Qdrant Collection Already Exists")


async def store_chunks(
    chunks,
    embeddings,
    owner,
    repo,
):
    client = await get_qdrant_client()

    print("🚀 store_chunks() called")
    print("Owner:", owner)
    print("Repo:", repo)

    points = []

    for chunk, embedding in zip(chunks, embeddings):

        points.append(
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "text": chunk["text"],
                    "repo": repo,
                    "owner": owner,
                    **chunk["metadata"],
                },
            )
        )

    await client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    count = await client.count(
        collection_name=COLLECTION_NAME,
    )

    print(f"✅ Stored {len(points)} vectors")
    print("Total vectors:", count.count)


async def repository_exists(
    owner: str,
    repo: str,
) -> bool:

    client = await get_qdrant_client()

    response = await client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
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
        limit=1,
        with_payload=False,
        with_vectors=False,
    )

    points, _ = response

    return len(points) > 0