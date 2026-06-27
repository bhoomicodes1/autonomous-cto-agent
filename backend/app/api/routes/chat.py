from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

from app.graph.workflow import workflow

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    result = await workflow.ainvoke(
    {
        "question": request.query,
        "owner": request.owner,
        "repo": request.repo,
        "intent": "",
        "chunks": [],
        "context": "",
        "mcp_context": "",
        "answer": "",
    }
)

    return ChatResponse(
        answer=result["answer"],
        sources=result["chunks"],
    )