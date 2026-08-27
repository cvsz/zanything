"""Application configuration and environment settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Enterprise application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="ZANYTHING_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "zanything"
    app_version: str = "0.1.0"
    env: Literal["development", "test", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_json: bool = True

    host: str = "0.0.0.0"
    port: int = 8080
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8080"]
    )

    # Security & Execution limits
    max_objective_length: int = 20000
    request_timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
