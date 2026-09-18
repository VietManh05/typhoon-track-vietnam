"""Central, environment-based application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and a local .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "typhoon-vn-forecast-system"
    app_env: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"
    log_level: str = "INFO"
    operational_database_url: str = "sqlite:///data/operational/typhoon.db"
    model_artifact: Path | None = None
    allow_baseline: bool = True
    api_key: str = ""
    requests_per_minute: int = 120
    cache_enabled: bool = False

    data_dir: Path = Path("data")
    model_registry_uri: str = "./mlruns"
    feature_store_dir: Path = Path("data/processed/features")

    database_url: str = "postgresql+psycopg://typhoon:typhoon@localhost:5432/typhoon"
    redis_url: str = "redis://localhost:6379/0"
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "typhoon-checkpoints"


@lru_cache
def get_settings() -> Settings:
    """Create one settings object per process."""

    return Settings()
