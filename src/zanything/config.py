"""Application configuration and environment settings."""

from functools import lru_cache
from typing import Any, Literal

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
    app_version: str = "1.0.0"
    env: Literal["development", "test", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_json: bool = True

    host: str = "0.0.0.0"
    port: int = 8080
    allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:8080"]
    )

    # Durable Data Runtime (PostgreSQL / SQLite fallback for local test)
    database_url: str = "sqlite+aiosqlite:///./zanything.db"

    # Security & Authentication (OIDC / JWT)
    allow_anonymous: bool = (
        True  # Allows unauthenticated requests to public endpoints if enabled
    )
    jwt_secret_key: str | None = "dev-secret-key-do-not-use-in-prod-1234567890123456"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_uri: str | None = None

    # Service Account API Keys registry mapping key to subject, roles & scopes
    service_account_api_keys: dict[str, dict[str, Any]] = Field(
        default_factory=lambda: {
            "test-sa-key-123": {
                "subject": "ci-service-account",
                "tenant_id": "tenant-corp-a",
                "roles": ["admin", "operator"],
                "scopes": ["*"],
            }
        }
    )

    # Security & Execution limits
    max_objective_length: int = 20000
    request_timeout_seconds: int = 30


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
