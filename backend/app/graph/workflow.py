from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.graph.state import AgentState

from app.agents.router import router
from app.agents.retriever import retriever
from app.agents.reviewer import reviewer
from app.agents.planner import planner
from app.agents.mcp import mcp


builder = StateGraph(AgentState)

builder.add_node("router", router)
builder.add_node("retriever", retriever)
builder.add_node("mcp", mcp)
builder.add_node("reviewer", reviewer)
builder.add_node("planner", planner)


builder.add_edge(
    START,
    "router",
)

builder.add_edge(
    "router",
    "retriever",
)

builder.add_edge(
    "retriever",
    "mcp",
)

builder.add_edge(
    "mcp",
    "reviewer",
)

builder.add_edge(
    "reviewer",
    "planner",
)

builder.add_edge(
    "planner",
    END,
)

workflow = builder.compile()