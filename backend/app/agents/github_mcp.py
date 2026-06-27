from app.graph.state import AgentState
from app.services.github_services import read_file


FILE_MAP = {
    "stategraph": "libs/langgraph/langgraph/graph/state.py",
    "pregel": "libs/langgraph/langgraph/pregel/main.py",
    "toolnode": "libs/prebuilt/langgraph/prebuilt/tool_node.py",
    "memory": "libs/checkpoint/langgraph/checkpoint/memory.py",
}


async def github_mcp(state: AgentState):

    question = state["question"].lower()

    github_context = ""

    for key, path in FILE_MAP.items():

        if key in question:

            print(f"\n📄 Fetching GitHub file: {path}")

            github_context = await read_file(
                owner="langchain-ai",
                repo="langgraph",
                path=path,
            )

            break

    return {
        "github_context": github_context
    }