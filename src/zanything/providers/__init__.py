"""Provider capability contracts, model specifications, and telemetry models."""

import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class ProviderType(StrEnum):
    """Supported LLM / AI providers."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    VERTEX = "vertex"
    LOCAL = "local"


class ModelSpec(BaseModel):
    """Specification of a specific provider model."""

    model_id: str
    provider: ProviderType
    context_window: int = 128000
    supports_vision: bool = True
    supports_tools: bool = True
    input_cost_per_million: float = 1.50
    output_cost_per_million: float = 6.00


class ProviderRequest(BaseModel):
    """Standardized model inference request."""

    messages: list[dict[str, Any]]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout_seconds: float = 30.0
    tenant_id: str = "default"


class ProviderResponse(BaseModel):
    """Standardized inference result with cost and token usage."""

    content: str
    model: str
    provider: ProviderType
    prompt_tokens: int
    completion_tokens: int
    total_cost_usd: float
    latency_ms: float
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
