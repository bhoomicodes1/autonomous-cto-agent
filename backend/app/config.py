from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # ==========================================
    # Application
    # ==========================================
    app_name: str = "Autonomous Startup CTO Agent"
    debug: bool = True

    # ==========================================
    # Gemini
    # ==========================================
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    # ==========================================
    # Production URLs (Render / Cloud)
    # ==========================================
    database_url: str | None = None
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    redis_url: str | None = None

    github_token: str | None = None

    # ==========================================
    # PostgreSQL (Local Docker)
    # ==========================================
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "cto_agent"
    postgres_user: str = "postgres"
    postgres_password: str

    @property
    def database_url_resolved(self):
        if self.database_url:
            return self.database_url.replace(
                "postgresql://",
                "postgresql+asyncpg://",
            ).replace(
                "postgres://",
                "postgresql+asyncpg://",
            )

        return (
            f"postgresql+asyncpg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    # ==========================================
    # Qdrant
    # ==========================================
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection: str = "architecture_docs"

    # ==========================================
    # Redis
    # ==========================================
    redis_host: str = "redis"
    redis_port: int = 6379

    # ==========================================
    # RAG Settings
    # ==========================================
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5


@lru_cache
def get_settings():
    return Settings()