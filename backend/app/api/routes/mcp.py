from fastapi import APIRouter

from app.mcp.github_mcp import read_github_file

router = APIRouter(
    prefix="/mcp",
    tags=["MCP"],
)


@router.get("/github/file")
async def github_file(
    owner: str,
    repo: str,
    path: str,
):

    content = await read_github_file(
        owner,
        repo,
        path,
    )

    return {
        "content": content
    }