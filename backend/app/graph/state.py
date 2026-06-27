from typing import TypedDict

class AgentState(TypedDict):

    question: str

    intent: str

    chunks: list

    context: str

    mcp_context: str

    answer: str
    owner: str
    repo: str