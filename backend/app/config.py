from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    # App
    app_name: str = "Autonomous Startup CTO Agent"
    debug: bool = True

    # Gemini
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    # PostgreSQL
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "cto_agent"
    postgres_user: str = "postgres"
    postgres_password: str

    github_token: str | None = None
    
    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    # Qdrant
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection: str = "architecture_docs"

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379

    # RAG
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5


@lru_cache
def get_settings():
    return Settings()