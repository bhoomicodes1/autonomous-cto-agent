from app.services.github_services import get_repo_tree


async def calculate_health(owner: str, repo: str):

    files = await get_repo_tree(owner, repo)

    # get_repo_tree() returns list of dictionaries
    names = []

    for f in files:
        if isinstance(f, dict):
            if "path" in f:
                names.append(f["path"].lower())
            elif "name" in f:
                names.append(f["name"].lower())
        elif isinstance(f, str):
            names.append(f.lower())

    checks = {
        "README": any("readme" in f for f in names),
        "Docker": any("dockerfile" in f for f in names),
        "Requirements": any(
            dep in f
            for f in names
            for dep in [
                "requirements.txt",
                "pyproject.toml",
                "package.json",
            ]
        ),
        "Tests": any(
            "test" in f or "tests" in f
            for f in names
        ),
        "GitHub Actions": any(
            ".github/workflows" in f
            for f in names
        ),
        "License": any(
            "license" in f
            for f in names
        ),
    }

    score = sum(checks.values()) * 15

    return {
        "overall": min(score, 100),
        "checks": checks,
    }