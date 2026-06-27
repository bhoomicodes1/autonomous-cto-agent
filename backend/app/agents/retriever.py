from app.graph.state import AgentState
from app.core.rag.retriever import retrieve


async def retriever(state: AgentState):

    chunks = await retrieve(
        query=state["question"],
        owner=state["owner"],
        repo=state["repo"],
    )

    context_parts = []

    for chunk in chunks:

        context_parts.append(
            f"""
========================================
FILE: {chunk['file']}
CHUNK: {chunk['chunk_index']}
SIMILARITY: {chunk['score']:.3f}
========================================

{chunk['text']}
"""
        )

    context = "\n\n".join(context_parts)

    return {
        "chunks": chunks,
        "context": context,
    }