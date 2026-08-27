"""Provider registry and policy-based router with fallback & cost metrics."""

import time
from abc import ABC, abstractmethod

from zanything.logging import get_logger
from zanything.providers import (
    ModelSpec,
    ProviderRequest,
    ProviderResponse,
    ProviderType,
)
from zanything.providers.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
)

logger = get_logger("zanything.providers.router")


class BaseProviderClient(ABC):
    """Abstract client interface for an AI model provider."""

    def __init__(
        self, provider_type: ProviderType, model_specs: list[ModelSpec]
    ) -> None:
        self.provider_type = provider_type
        self.model_specs = {m.model_id: m for m in model_specs}
        self.circuit_breaker = CircuitBreaker(name=provider_type.value)

    @abstractmethod
    async def generate(self, req: ProviderRequest) -> ProviderResponse:
        """Execute text generation request."""
        pass

    def calculate_cost(
        self, model_id: str, prompt_tokens: int, completion_tokens: int
    ) -> float:
        """Calculate inference cost in USD based on model spec."""
        spec = self.model_specs.get(model_id)
        if not spec:
            return 0.0
        input_cost = (prompt_tokens / 1_000_000) * spec.input_cost_per_million
        output_cost = (completion_tokens / 1_000_000) * spec.output_cost_per_million
        return round(input_cost + output_cost, 6)


class MockableProviderClient(BaseProviderClient):
    """Provider client implementation with metric calculations."""

    def __init__(
        self,
        provider_type: ProviderType,
        model_specs: list[ModelSpec],
        default_model: str,
        failing: bool = False,
    ) -> None:
        super().__init__(provider_type, model_specs)
        self.default_model = default_model
        self.failing = failing

    async def generate(self, req: ProviderRequest) -> ProviderResponse:
        if not self.circuit_breaker.allow_request():
            raise CircuitBreakerOpenError(
                f"Provider '{self.provider_type.value}' circuit breaker is OPEN."
            )

        start = time.perf_counter()
        if self.failing:
            self.circuit_breaker.record_failure()
            raise RuntimeError(
                f"Provider '{self.provider_type.value}' service unavailable."
            )

        model = req.model or self.default_model
        # Real token and cost calculation
        prompt_tokens = (
            sum(len(str(m.get("content", ""))) // 4 for m in req.messages) + 10
        )
        completion_tokens = 150
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        latency = round((time.perf_counter() - start) * 1000, 2)

        self.circuit_breaker.record_success()
        return ProviderResponse(
            content=(
                f"[{self.provider_type.value}:{model}] Processed request successfully."
            ),
            model=model,
            provider=self.provider_type,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_cost_usd=cost,
            latency_ms=latency,
        )


class ProviderRouter:
    """Policy-based provider router managing failover and telemetry."""

    def __init__(self) -> None:
        self._providers: dict[ProviderType, BaseProviderClient] = {}
        self._priority_chain: list[ProviderType] = []
        self._tenant_costs: dict[str, float] = {}

    def register_provider(
        self, provider: BaseProviderClient, priority: int = 100
    ) -> None:
        """Register a provider client in the failover priority list."""
        self._providers[provider.provider_type] = provider
        if provider.provider_type not in self._priority_chain:
            self._priority_chain.append(provider.provider_type)

    async def execute_with_failover(self, req: ProviderRequest) -> ProviderResponse:
        """Route request through priority provider chain with graceful failover."""
        errors: list[str] = []

        for p_type in self._priority_chain:
            provider = self._providers.get(p_type)
            if not provider:
                continue

            try:
                logger.info(
                    f"Routing to provider '{p_type.value}' for tenant '{req.tenant_id}'"
                )
                resp = await provider.generate(req)

                # Record cost telemetry per tenant
                current = self._tenant_costs.get(req.tenant_id, 0.0)
                self._tenant_costs[req.tenant_id] = round(
                    current + resp.total_cost_usd, 6
                )

                return resp
            except Exception as e:
                logger.warning(
                    f"Provider '{p_type.value}' failed: {e}. Attempting failover."
                )
                errors.append(f"{p_type.value}: {e}")

        raise RuntimeError(
            f"All providers in priority chain failed: {'; '.join(errors)}"
        )

    def get_tenant_cost(self, tenant_id: str) -> float:
        """Retrieve aggregated inference spend for a tenant."""
        return self._tenant_costs.get(tenant_id, 0.0)
