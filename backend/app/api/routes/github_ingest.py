from fastapi import APIRouter

from app.services.github_ingestion import load_repository

router = APIRouter(
    prefix="/github-ingest",
    tags=["GitHub"],
)


@router.post("/")
async def ingest_repo(owner: str, repo: str):

    result = await load_repository(
        owner,
        repo,
    )

    return result