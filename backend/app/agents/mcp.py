from app.graph.state import AgentState

from app.services.github_search import search_repository
from app.services.github_services import read_file


async def mcp(state: AgentState):

    print("\n========== GITHUB SEARCH ==========")

    owner = state["owner"]
    repo = state["repo"]

    files = await search_repository(
        owner,
        repo,
        state["question"],
    )

    print(files)

    context = ""

    for file in files:

        path = file.get("path", "")

        if not path:
            continue

        print("Reading:", path)

        try:

            text = await read_file(
                owner,
                repo,
                path,
            )

        except Exception as e:

            print(f"❌ MCP Error while reading {path}: {e}")
            continue

        context += f"""

========================
FILE:
{path}
========================

{text[:4000]}
"""

    print("\n========== MCP FINISHED ==========\n")

    return {
        "mcp_context": context,
    }