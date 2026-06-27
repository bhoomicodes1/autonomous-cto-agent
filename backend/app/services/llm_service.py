from google import genai
from google.genai.errors import ServerError
import asyncio

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

        system_prompt = ANALYSIS_PROMPT

    else:

        system_prompt = SYSTEM_PROMPT

    prompt = f"""
{system_prompt}

==========================
REPOSITORY CONTEXT
==========================

{context}

==========================
USER QUESTION
==========================

{question}

IMPORTANT:

- Use ONLY the repository context above.
- If the answer is not present in the context, say:
  "The retrieved repository context does not contain enough information."
- Mention relevant file names whenever possible.
- Never answer using general FastAPI, Python, or programming knowledge if the context already contains the answer.
"""

    for attempt in range(3):
        try:

            response = client.models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
            )

            if response.text:
                return response.text

            return "No answer generated."

        except ServerError:
            print("Gemini busy...")
            await asyncio.sleep(5)

        except Exception as e:
            print(e)

            if "RESOURCE_EXHAUSTED" in str(e):
                return """
# ⚠ Gemini Rate Limit Reached

The free Gemini API quota has been exhausted.

Please wait a minute and try again.

Repository indexing completed successfully.
"""

            return f"Error: {e}"

    return "Gemini unavailable."

async def analyze_repository(readme: str):

    prompt = f"""
You are a Senior Staff AI Engineer.

Analyze this GitHub repository README.

Return markdown in this format.

# 📌 Summary

# 🏗 Architecture

# 💻 Tech Stack

# 📂 Folder Structure (if mentioned)

# 🚀 Features

# ⚠ Technical Debt

# 📈 Scalability

# 🔐 Security

# 🎯 CTO Recommendations

README

{readme}
"""

    print("="*80)
    print(prompt[:4000])
    print("="*80)
    
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
    )

    return response.text