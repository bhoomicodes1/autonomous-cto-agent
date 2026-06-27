import httpx

GITHUB_API = "https://api.github.com"


async def read_github_file(
    owner: str,
    repo: str,
    path: str,
):

    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"

    async with httpx.AsyncClient(
    timeout=120,
    follow_redirects=True,
    ) as client:

        response = await client.get(url)

        response.raise_for_status()

        data = response.json()

    import base64

    if data["encoding"] == "base64":
        return base64.b64decode(
            data["content"]
        ).decode()

    return ""