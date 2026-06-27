import httpx
import asyncio

from app.core.rag.chunker import chunk_document
from app.core.rag.embedder import embed_texts
from app.core.vectorstore.qdrant_store import store_chunks
from app.services.github_services import get_repo_files

RAW_BASE = "https://raw.githubusercontent.com"

IGNORE_DIRS = (
    "tests/",
    "test/",
    "fixtures/",
    ".github/",
    "__pycache__",
    "examples/",
    "example_app/",
    "benchmarks/",
    "docs/api/",
)

ALLOWED_EXTENSIONS = (
    ".py",
    ".md",
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

# Skip noisy files/folders
IGNORE_FOLDERS = (
    "tests/",
    "test/",
    "fixtures/",
    ".github/",
    "__pycache__/",
    "examples/",
    "docs/api/",
    "docs/docs/",
    "node_modules/",
)

IGNORE_FILES = (
    "requirements.txt",
    "poetry.lock",
    "package-lock.json",
    "yarn.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Cargo.lock",
)


async def download_file(owner: str, repo: str, path: str):

    url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}"

    timeout = httpx.Timeout(120.0)

    async with httpx.AsyncClient(timeout=timeout) as client:

        for attempt in range(3):

            try:

                response = await client.get(url)

                if response.status_code == 200:
                    return response.text

                return ""

            except httpx.ReadTimeout:

                print(f"⏳ Timeout ({attempt+1}/3): {path}")

                await asyncio.sleep(2)

            except Exception as e:

                print(f"❌ Error downloading {path}: {e}")

                return ""

    print(f"⛔ Skipping {path}")

    return ""

async def load_repository(owner: str, repo: str):

    tree = await get_repo_files(owner, repo)
    print("TREE =", tree)
    print("FILES =", len(tree["files"]))
    total_chunks = 0
    total_files = 0

    for item in tree["files"]:
        print("Checking:", item["path"])
        if item["type"] != "blob":
            continue

        path = item["path"]

        if any(ignore in path for ignore in IGNORE_DIRS):
            print("Ignored directory:", path)
            continue
          
        if not path.endswith(ALLOWED_EXTENSIONS):
            print("Extension rejected:", path)
            continue

        # Skip noisy folders
        if path.startswith(IGNORE_FOLDERS):
            print("Folder rejected:", path)
            continue

        # Skip noisy files
        if path.endswith(IGNORE_FILES):
            print("File rejected:", path)
            continue

        print(f"Downloading {path}")

        text = await download_file(owner, repo, path)
        if not text:
            continue
        
        print(path, "Length:", len(text))

        if len(text.strip()) < 30:
            continue
        
        if len(text) > 100000:
            print("Huge file skipped")
            continue
        
        chunks = chunk_document(
            text=text,
            doc_id=path,
        )

        embeddings = await embed_texts(
            [c["text"] for c in chunks]
        )
        print("About to store:", path)
        await store_chunks(
            chunks,
            embeddings,
            owner,
            repo,
)

        total_chunks += len(chunks)
        total_files += 1

        print(f"Stored {path}")

    return {
        "files": total_files,
        "chunks": total_chunks,
    }
    