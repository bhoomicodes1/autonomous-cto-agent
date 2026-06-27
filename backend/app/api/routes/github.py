from fastapi import APIRouter

from app.core.rag.retriever import retrieve
from app.core.vectorstore.qdrant_store import repository_exists
from app.services.github_ingestion import load_repository
from app.services.llm_service import ask_llm
from app.services.github_services import get_repo_tree
from app.services.repository_health import calculate_health
from app.services.dependency_graph import get_dependency_graph
from app.services.architecture_graph import generate_architecture

router = APIRouter(
    prefix="/github",
    tags=["GitHub"],
)


@router.post("/analyze")
async def analyze_repo(
    owner: str,
    repo: str,
):
    """
    Analyze the already-ingested repository using Qdrant.
    """

    query = f"""
Analyze the architecture of the GitHub repository {owner}/{repo}.

Explain:

- Project Summary
- Architecture
- Tech Stack
- Folder Structure
- Important Files
- Code Flow
- Features
- Technical Debt
- Scalability
- Security
- CTO Recommendations
- Interview Questions
"""

    indexed = await repository_exists(
        owner,
        repo,
)

    if not indexed:

        print(f"📥 {owner}/{repo} not indexed. Starting ingestion...")

        await load_repository(
            owner,
            repo,
    )

    print("✅ Repository indexed successfully.")
    print("🔍 Starting retrieval")
    chunks = await retrieve(
    query=query,
    owner=owner,
    repo=repo,
    limit=25,
)

    context = "\n\n".join(
        [
            f"""
FILE: {c['file']}
CHUNK: {c['chunk_index']}

{c['text']}
"""
            for c in chunks
        ]
    )
    health = await calculate_health(owner, repo)
    answer = await ask_llm(
    question=query,
    context=context,
    mode="analysis",
)

    return {
    "analysis": answer,
    "health": health,
}


@router.post("/files")
async def github_files(
    owner: str,
    repo: str,
):

    files = await get_repo_tree(
        owner,
        repo,
    )

    return {
        "total_files": len(files),
        "files": files,
    }
    
@router.get("/dependency-graph")
async def dependency_graph(
    owner: str,
    repo: str,
):

    tree = await get_dependency_graph(
        owner,
        repo,
    )

    return tree

@router.get("/architecture")
async def architecture(
    owner: str,
    repo: str,
):
    return await generate_architecture(owner, repo)