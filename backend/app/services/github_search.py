from app.services.github_services import get_repo_tree

IMPORTANT_FILES = [
    "README.md",
    "docs",
    "concepts",
    "reference",
    "libs/langgraph",
]


async def search_repository(
    owner: str,
    repo: str,
    query: str,
):
    print("\n========== GITHUB SEARCH ==========")

    tree = await get_repo_tree(owner, repo)

    print(f"Total files in repo: {len(tree)}")

    keywords = [
        word.lower()
        for word in query.split()
        if len(word) > 2
    ]

    print("Keywords:", keywords)

    important_words = [
        "graph",
        "state",
        "pregel",
        "checkpoint",
        "memory",
        "agent",
        "node",
    ]

    matches = []

    for file in tree:

        # Skip folders
        if file["type"] != "blob":
            continue

        path = file["path"]
        lower = path.lower()

        score = 0

        # Query keyword match
        for keyword in keywords:
            if keyword in lower:
                score += 3

        # Important architecture files
        for word in important_words:
            if word in lower:
                score += 2

        # README / Docs bonus
        for imp in IMPORTANT_FILES:
            if imp.lower() in lower:
                score += 2

        # Markdown bonus
        if lower.endswith(".md"):
            score += 2

        # Python bonus
        if lower.endswith(".py"):
            score += 1

        # IMPORTANT:
        # Do NOT restrict to only .py files.
        if score > 0:
            matches.append(
                {
                    "path": path,
                    "score": score,
                }
            )

    matches.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    print("\n===== MATCHED FILES =====")

    for m in matches[:10]:
        print(m)

    print("=========================\n")

    return matches[:10]