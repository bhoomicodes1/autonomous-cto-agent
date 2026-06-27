from app.services.github_services import get_repo_tree


async def generate_architecture(owner: str, repo: str):
    files = await get_repo_tree(owner, repo)

    nodes = []
    edges = []

    root = f"{owner}/{repo}"
    nodes.append({"id": root})

    for file in files:

        if isinstance(file, dict):
            path = file.get("path", "")
        else:
            path = file

        if not path:
            continue

        parts = path.split("/")

        parent = root

        current = ""

        for part in parts:

            current = f"{current}/{part}" if current else part

            if not any(n["id"] == current for n in nodes):
                nodes.append({"id": current})

            edges.append({
                "source": parent,
                "target": current,
            })

            parent = current

    return {
        "nodes": nodes,
        "edges": edges,
    }