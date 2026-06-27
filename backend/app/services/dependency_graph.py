from app.services.github_services import get_repo_tree


async def get_dependency_graph(owner: str, repo: str):

    files = await get_repo_tree(owner, repo)

    tree = {}

    for file in files:

        # get_repo_tree may return dicts or strings
        if isinstance(file, dict):
            path = file.get("path", "")
        else:
            path = file

        if not path:
            continue

        parts = path.split("/")

        current = tree

        for part in parts[:-1]:
            current = current.setdefault(part, {})

        current.setdefault("__files__", []).append(parts[-1])

    return tree