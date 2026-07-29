from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "KAIROS"
    app_version: str = "1.0.0"
    app_env: str = "development"
    log_level: str = "INFO"

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "kairos_db"
    database_user: str = "kairos_user"
    database_password: str = "kairos_password"
    database_echo: bool = False

    jwt_secret_key: str = (
        "kairos_super_secret_development_key_change_in_production_1234567890"
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Redis Settings
    redis_url: str = "redis://redis:6379/0"

    # AI Configuration
    ai_enabled: bool = True
    ai_provider: str = "groq"
    ai_default_model: str = "llama-3.3-70b-versatile"
    ai_timeout: int = 60
    ai_max_retries: int = 3
    ai_streaming: bool = True
    
    groq_api_key_1: str = ""
    groq_api_key_2: str = ""
    groq_api_key_3: str = ""
    groq_api_key_4: str = ""
    groq_api_key_5: str = ""

    # Embedding and RAG
    embedding_provider: str = "local"
    embedding_model: str = "nomic-embed-text"
    rag_top_k: int = 5
    rag_max_chunks: int = 8
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Cache and Token Limits
    ai_cache_enabled: bool = True
    ai_cache_ttl: int = 3600
    ai_max_input_tokens: int = 16000
    ai_max_output_tokens: int = 4096

    # Prompts
    prompt_version: str = "latest"

    # Celery
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    # Rate Limiting
    ai_requests_per_minute: int = 60
    ai_requests_per_hour: int = 1000

    # Observability
    enable_prometheus: bool = True
    enable_tracing: bool = True
    enable_metrics: bool = True

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )


settings = Settings()
