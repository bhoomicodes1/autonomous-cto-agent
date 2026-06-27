from app.graph.state import AgentState
from app.services.llm_service import ask_llm


async def planner(state: AgentState):

    print("\n========== PLANNER ==========")
    print("QUESTION:", state["question"])

    print("\n========== FINAL CONTEXT ==========")
    print(state["context"][:1000])
    print("===================================\n")

    answer = await ask_llm(
    question=state["question"],
    context=state["context"],
    mode="chat",
)

    print("\n========== ANSWER ==========")
    print(answer)
    print("============================\n")

    return {
        "answer": answer,
    }