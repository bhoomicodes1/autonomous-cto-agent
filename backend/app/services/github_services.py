import base64
import httpx


GITHUB_API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Autonomous-CTO-Agent",
}


async def get_repo_tree(owner: str, repo: str):
    """
    Returns all files in the repository recursively.
    """

    async with httpx.AsyncClient(
    timeout=120,
    follow_redirects=True,
    ) as client:

        # Step 1: Get repository metadata
        repo_response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=HEADERS,
        )

        repo_response.raise_for_status()

        default_branch = repo_response.json()["default_branch"]

        # Step 2: Fetch tree using the actual default branch
        tree_response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1",
            headers=HEADERS,
        )

        tree_response.raise_for_status()

        return tree_response.json().get("tree", [])
    
    
async def read_file(owner: str, repo: str, path: str):
    """
    Reads a single file from GitHub repository.
    """

    async with httpx.AsyncClient(
    timeout=120,
    follow_redirects=True,
    ) as client:

        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            headers=HEADERS,
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return ""

        if data.get("encoding") == "base64":

            try:
                return base64.b64decode(
                    data["content"]
                ).decode(
                    "utf-8",
                    errors="ignore",
                )

            except Exception as e:
                print(f"Decode Error ({path}):", e)
                return ""

        return ""


async def get_repo_files(owner: str, repo: str):
    """
    Returns repository in a format compatible with github_ingestion.py
    """

    tree = await get_repo_tree(owner, repo)

    return {
        "total_files": len(tree),
        "files": tree,
    }


async def get_readme(owner: str, repo: str):
    """
    Reads the repository README file.
    """

    candidates = [
        "README.md",
        "Readme.md",
        "readme.md",
    ]

    for filename in candidates:

        try:

            content = await read_file(
                owner,
                repo,
                filename,
            )

            if content:
                return content

        except Exception as e:

            print(f"README Error ({filename}):", e)

    return "README not found."