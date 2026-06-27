from app.graph.state import AgentState

DOC_KEYWORDS = [
    "langgraph",
    "langchain",
    "pregel",
    "stategraph",
    "graph",
    "node",
    "edge",
    "agent",
    "workflow",
    "checkpoint",
    "memory",
    "tool",
    "toolnode",
    "mcp",
    "github",
    "architecture",

    # Repository questions
    "file",
    "folder",
    "class",
    "function",
    "method",
    "api",
    "endpoint",
    "fastapi",
    "main",
    "entry",
    "repository",
    "repo",
    "code",
    "module",
    "service",
    "database",
    "route",
    "router",
    "model",
    "authentication",
    "authorization",
    "security",
]

async def router(state: AgentState):

    question = state["question"].lower()

    if any(keyword in question for keyword in DOC_KEYWORDS):
        intent = "docs"
    else:
        intent = "general"

    print(f"\n🧠 Intent: {intent}")
    print(f"Question: {question}\n")

    return {
        "intent": intent,
    }