from sentence_transformers import SentenceTransformer

_model = None


def get_embedding_model() -> SentenceTransformer:
    """
    Singleton model.
    Model sirf ek baar RAM me load hoga.
    """
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts.
    """
    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    return embeddings.tolist()