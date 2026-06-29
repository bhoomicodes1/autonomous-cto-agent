from google import genai

from app.config import get_settings
from app.core.prompts.cto_prompt import SYSTEM_PROMPT
from app.core.prompts.analysis_prompt import ANALYSIS_PROMPT

settings = get_settings()

client = genai.Client(
    api_key=settings.gemini_api_key,
)


async def ask_llm(
    question: str,
    context: str,
    mode: str = "chat",
) -> str:

    if mode == "analysis":
        instruction = ANALYSIS_PROMPT
    else:
        instruction = SYSTEM_PROMPT

    prompt = f"""
{instruction}

Repository Context

{context}

User Request

{question}

IMPORTANT

Never include function implementations.

Never quote source code.

Summarize implementation only.

Maximum 2-3 filenames per section.

Never generate Sources.
Never generate Suggested Questions.
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text