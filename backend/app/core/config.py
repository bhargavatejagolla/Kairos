from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_env: str
    log_level: str

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str
    database_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}"
            f"/{self.database_name}"
        )


settings = Settings()
