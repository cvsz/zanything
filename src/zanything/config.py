"""Application configuration and environment settings."""

from functools import lru_cache
from typing import Any, Literal

from pydantic import Field, model_validator
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
    app_version: str = "1.0.1"
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
    allow_anonymous: bool = True
    jwt_secret_key: str | None = "dev-secret-key-do-not-use-in-prod-1234567890123456"
    oidc_issuer: str | None = None
    oidc_audience: str | None = None
    oidc_jwks_uri: str | None = None

    # Cloudflare Access Zero Trust authentication. Forwarded identity headers are
    # accepted only when accompanied by a JWT assertion verified with these values.
    cloudflare_access_enabled: bool = False
    cloudflare_access_issuer: str | None = None
    cloudflare_access_audience: str | None = None
    cloudflare_access_jwks_uri: str | None = None

    # Service Account API Keys registry mapping key to subject, roles & scopes.
    # Demo keys are permitted only outside production and are rejected by validation.
    service_account_api_keys: dict[str, dict[str, Any]] = Field(
        default_factory=lambda: {
            "test-sa-key-123": {
                "subject": "ci-service-account",
                "tenant_id": "tenant-corp-a",
                "roles": ["admin", "operator"],
                "scopes": ["*"],
            },
            "zany-admin-demo-key": {
                "subject": "admin-operator",
                "tenant_id": "zeaz-enterprise",
                "roles": ["admin", "operator", "auditor", "viewer"],
                "scopes": ["*"],
            },
            "zany-auditor-demo-key": {
                "subject": "security-auditor",
                "tenant_id": "zeaz-enterprise",
                "roles": ["auditor", "viewer"],
                "scopes": ["read", "audit"],
            },
        }
    )

    # Security & Execution limits
    max_objective_length: int = 20000
    request_timeout_seconds: int = 30

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        """Fail closed when production is started with development auth defaults."""
        if self.env != "production":
            return self

        if self.allow_anonymous:
            raise ValueError("ZANYTHING_ALLOW_ANONYMOUS must be false in production")

        if self.jwt_secret_key and "dev-secret-key-do-not-use-in-prod" in self.jwt_secret_key:
            raise ValueError("development JWT secret must not be used in production")

        demo_keys = {
            "test-sa-key-123",
            "zany-admin-demo-key",
            "zany-auditor-demo-key",
        }
        if demo_keys.intersection(self.service_account_api_keys):
            raise ValueError("demo service-account API keys must not be used in production")

        oidc_ready = bool(self.oidc_issuer and self.oidc_audience and self.oidc_jwks_uri)
        cf_ready = bool(
            self.cloudflare_access_enabled
            and self.cloudflare_access_issuer
            and self.cloudflare_access_audience
            and self.cloudflare_access_jwks_uri
        )
        service_accounts_ready = bool(self.service_account_api_keys)

        if not (oidc_ready or cf_ready or service_accounts_ready):
            raise ValueError(
                "production requires OIDC, verified Cloudflare Access, or configured service-account authentication"
            )

        if self.cloudflare_access_enabled and not cf_ready:
            raise ValueError(
                "Cloudflare Access requires issuer, audience, and JWKS URI in production"
            )

        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton."""
    return Settings()
