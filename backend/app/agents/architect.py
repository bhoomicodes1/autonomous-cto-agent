from app.graph.state import AgentState
from app.services.llm_service import ask_llm


async def architect(state: AgentState):

    answer = await ask_llm(
        question=state["question"],
        context=state["context"],
    )

    return {
        **state,
        "answer": answer,
    }