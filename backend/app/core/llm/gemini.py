from google import genai

from app.config import get_settings

settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key,
)


async def ask_gemini(context: str, question: str) -> str:

    prompt = f"""
You are a Senior Staff Software Architect.

Answer ONLY using the provided context.

If the answer is not present in the context, say:
"I couldn't find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text