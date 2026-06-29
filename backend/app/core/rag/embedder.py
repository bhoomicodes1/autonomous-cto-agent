from google import genai

from app.config import get_settings

settings = get_settings()
print("Gemini key starts with:", settings.gemini_api_key[:10])

client = genai.Client(
    api_key=settings.gemini_api_key,
)


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings using Gemini.
    """

    embeddings = []

    for text in texts:
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
        )

        embeddings.append(response.embeddings[0].values)

    return embeddings