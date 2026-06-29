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

Task

Generate a professional software architecture report.

Rules

- Use ONLY the repository context.
- Never invent files.
- Never output Sources.
- Never output Repository Health.
- Never output Suggested Questions.
- Never output Interview Questions.
- Never output Prompt files.
- Never mention analysis_prompt.py.
- Never mention cto_prompt.py.
- Never mention frontend/App.jsx unless essential.
- If details are missing, infer reasonable architecture decisions instead of saying "Not enough information."
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text