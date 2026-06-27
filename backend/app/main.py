from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

from app.db.qdrant import init_qdrant
from app.db.postgres import Base, engine

from app.core.vectorstore.qdrant_store import create_collection

from app.api.routes import (
    document_router,
    search_router,
    chat_router,
    github_router,
    github_ingest_router,
    mcp,
)

from app.api.routes.github_code_ingest import (
    router as github_code_router,
)

import app.core.langsmith


@asynccontextmanager
async def lifespan(app: FastAPI):

    settings = get_settings()

    # Initialize Qdrant
    await init_qdrant(settings)

    # Create Qdrant collection
    await create_collection()

    # Create PostgreSQL tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database Ready")
    print("✅ Qdrant Ready")
    print("✅ Application Started")

    yield

    print("🛑 Application Stopped")


app = FastAPI(
    title="Autonomous Startup CTO Agent",
    version="0.1.0",
    lifespan=lifespan,
)

# -------------------------------
# CORS
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Routers
# -------------------------------

app.include_router(document_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(github_router)
app.include_router(github_ingest_router)
app.include_router(mcp.router)
app.include_router(github_code_router)

# -------------------------------
# Health
# -------------------------------

@app.get("/")
async def root():
    return {
        "message": "CTO Agent Running 🚀"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }