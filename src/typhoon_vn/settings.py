"""Central, environment-based application configuration."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

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
    metrics_token_file: Path | None = None
    require_api_key: bool = False
    jwt_secret: str = ""
    jwt_issuer: str = "typhoon-vn"
    jwt_audience: str = "typhoon-vn-api"
    jwt_expiry_seconds: int = Field(default=3600, ge=60, le=86400)
    oauth_username: str = ""
    oauth_password: str = ""
    cors_origins: list[str] = Field(default_factory=list)
    requests_per_minute: int = Field(default=120, ge=1)
    cache_enabled: bool = False
    forecast_cache_ttl_seconds: int = Field(default=1800, ge=1, le=86400)
    forecast_cache_max_entries: int = Field(default=1024, ge=1, le=100000)
    log_json: bool = True
    slow_request_ms: int = Field(default=1000, ge=1)
    inference_max_concurrency: int = Field(default=4, ge=1, le=128)
    weather_provider: Literal["accuweather", "open-meteo"] = "open-meteo"
    accuweather_api_key: str = ""
    accuweather_base_url: str = "https://dataservice.accuweather.com"
    open_meteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    weather_request_timeout_seconds: float = Field(default=8.0, gt=0, le=60)
    weather_current_ttl_seconds: int = Field(default=600, ge=60, le=3600)
    weather_hourly_ttl_seconds: int = Field(default=1200, ge=300, le=7200)
    weather_daily_ttl_seconds: int = Field(default=7200, ge=1800, le=21600)
    weather_alerts_ttl_seconds: int = Field(default=300, ge=60, le=1800)
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

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, values: list[str]) -> list[str]:
        from urllib.parse import urlsplit

        for value in values:
            parsed = urlsplit(value)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.netloc
                or parsed.username
                or parsed.password
                or parsed.path
                or parsed.query
                or parsed.fragment
                or value == "*"
            ):
                raise ValueError("CORS_ORIGINS must contain exact HTTP(S) origins")
        return values

    @model_validator(mode="after")
    def production_is_fail_closed(self) -> "Settings":
        if self.app_env == "production":
            oauth_ready = bool(
                len(self.jwt_secret) >= 32
                and self.oauth_username
                and self.oauth_password
            )
            if not self.api_key and not oauth_ready:
                raise ValueError(
                    "Production requires API_KEY or OAuth credentials with a "
                    "JWT_SECRET of at least 32 characters"
                )
            if self.allow_baseline:
                raise ValueError("Production requires ALLOW_BASELINE=false")
        return self


@lru_cache
def get_settings() -> Settings:
    """Create one validated settings object per process."""
    return Settings()
