from fastapi import APIRouter

from app.services.github_ingestion import (
    load_repository,
)

router = APIRouter(
    prefix="/github-code",
    tags=["GitHub Code"],
)


@router.post("/ingest")
async def ingest(
    owner: str,
    repo: str,
):

    return await load_repository(
        owner,
        repo,
)