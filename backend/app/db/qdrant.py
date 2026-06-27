from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams

from app.config import Settings

_client: AsyncQdrantClient | None = None


async def init_qdrant(settings: Settings):
    """
    Initialize Qdrant client and create collection if needed.
    """
    global _client

    _client = AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )

    collections = await _client.get_collections()

    names = [c.name for c in collections.collections]

    if settings.qdrant_collection not in names:
        await _client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        print("✅ Qdrant collection created")


async def get_qdrant_client() -> AsyncQdrantClient:
    if _client is None:
        raise RuntimeError("Qdrant is not initialized")

    return _client