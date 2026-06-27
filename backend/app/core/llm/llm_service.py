from google import genai

from app.config import get_settings
from app.core.prompts.cto_prompt import SYSTEM_PROMPT

settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key,
)


async def ask_llm(question: str, context: str) -> str:
    """
    Send retrieved context + user question to Gemini.
    """

    prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:
{context}

User Question:
{question}

Answer only using the retrieved context.
If the answer is not present, say:
"I couldn't find that information in the provided documents."
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text
