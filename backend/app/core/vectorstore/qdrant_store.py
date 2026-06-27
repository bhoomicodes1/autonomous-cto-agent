from uuid import uuid4

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import (
    VectorParams,
    Distance,
    PointStruct,
)

from app.config import get_settings

settings = get_settings()

client = AsyncQdrantClient(
    host=settings.qdrant_host,
    port=settings.qdrant_port,
)

COLLECTION_NAME = "architecture_docs"


async def create_collection():

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
    print("🚀 store_chunks() called")
    print("Owner:", owner)
    print("Repo:", repo)
    print("Chunks:", len(chunks))
    print("Embeddings:", len(embeddings))
    
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
                }
            )
        )

    await client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    print(f"✅ Stored {len(points)} vectors in Qdrant")
 
    count = await client.count(
    collection_name=COLLECTION_NAME,
    )

    print("Total vectors in Qdrant:", count.count)
    
from qdrant_client.http.models import (
    Filter,
    FieldCondition,
    MatchValue,
)


async def repository_exists(
    owner: str,
    repo: str,
) -> bool:

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