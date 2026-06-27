from app.services.github_services import (
    get_repo_tree,
    read_file,
)

from app.core.rag.chunker import chunk_document
from app.core.rag.embedder import embed_texts
from app.core.vectorstore.qdrant_store import store_chunks


IGNORE_DIRS = {
    ".git",
    "tests",
    "__pycache__",
    ".github",
    "docs/static",
    "node_modules",
}


ALLOWED_EXTENSIONS = (
    ".py",
    ".md",
    ".ipynb",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".tsx",
    ".ts",
    ".js",
    ".jsx",
    ".html",
    ".css",
    ".scss",
    ".sql",
    ".env.example",
    ".dockerfile",
)


async def ingest_github_repository(
    owner: str,
    repo: str,
):

    tree = await get_repo_tree(owner, repo)

    total_files = 0
    total_chunks = 0

    for file in tree:

        if file["type"] != "blob":
            continue

        path = file["path"]

        if any(ignore in path for ignore in IGNORE_DIRS):
            continue

        if not path.endswith(ALLOWED_EXTENSIONS):
            continue

        print(f"Reading {path}")

        text = await read_file(
            owner,
            repo,
            path,
        )

        if not text.strip():
            continue

        chunks = chunk_document(
            text=text,
            doc_id=path,
        )

        embeddings = await embed_texts(
            [c["text"] for c in chunks]
        )

        await store_chunks(
            chunks,
            embeddings,
            owner,
            repo,
        )

        total_files += 1
        total_chunks += len(chunks)

    return {
        "files": total_files,
        "chunks": total_chunks,
    }