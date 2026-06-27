from app.graph.state import AgentState


async def reviewer(state: AgentState):

    unique = {}

    for chunk in state["chunks"]:
        key = f'{chunk["doc_id"]}_{chunk["chunk_index"]}'
        unique[key] = chunk

    chunks = sorted(
        unique.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    rag_context = "\n\n".join(
        chunk["text"]
        for chunk in chunks[:5]
    )

    combined_context = f"""
================ RAG CONTEXT ================

{rag_context}

================ GITHUB MCP CONTEXT ================

{state.get("mcp_context", "")}
"""

    return {
        "chunks": chunks,
        "context": combined_context,
        "mcp_context": state.get("mcp_context", ""),
    }