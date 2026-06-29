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
    Analyze an indexed repository using RAG.
    """

    query = """
Analyze THIS repository only.

Return EXACTLY these sections:

# Executive Summary

# Architecture

# Tech Stack

# Important Components

# Code Flow

# Security

# Scalability

# Technical Debt

# CTO Recommendations

Rules:

- Use markdown.
- Maximum 500 words.
- Mention filenames whenever possible.
- Never invent files.
- Never include Repository Health.
- Never include Suggested Questions.
- Never include Interview Questions.
- Never include Sources.
- Never quote source code.
- Never include function implementations.
- Summarize implementation only.
- Focus on architecture and design.
"""

    indexed = await repository_exists(owner, repo)

    if not indexed:

        print(f"📥 {owner}/{repo} not indexed. Starting ingestion...")

        await load_repository(
            owner,
            repo,
        )

    print("✅ Repository indexed.")
    print("🔍 Retrieving context...")

    chunks = await retrieve(
        query=query,
        owner=owner,
        repo=repo,
        limit=10,
    )

    context = ""

    for chunk in chunks:

        context += f"""

==================================================

FILE:
{chunk["file"]}

CHUNK:
{chunk["chunk_index"]}

CONTENT:

{chunk["text"][:700]}

"""

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