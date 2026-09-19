"""Central, environment-based application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime settings loaded from environment and .env."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
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
    requests_per_minute: int = Field(default=120, ge=1)
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

    @field_validator("app_env", mode="before")
    @classmethod
    def normalize_environment(cls, value: object) -> str:
        normalized = str(value).strip().casefold()
        if not normalized:
            raise ValueError("APP_ENV must not be empty")
        return normalized

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("API_PREFIX must start with '/'")
        return value.rstrip("/") or "/"

    @field_validator("log_level", mode="before")
    @classmethod
    def normalize_log_level(cls, value: object) -> str:
        normalized = str(value).strip().upper()
        if normalized not in {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}:
            raise ValueError("LOG_LEVEL must be a standard Python logging level")
        return normalized

    @model_validator(mode="after")
    def production_is_fail_closed(self) -> "Settings":
        if self.app_env == "production" and (not self.api_key or self.allow_baseline):
            raise ValueError("Production requires API_KEY and ALLOW_BASELINE=false")
        return self


@lru_cache
def get_settings() -> Settings:
    """Create one validated settings object per process."""
    return Settings()
