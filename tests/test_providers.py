"""Tests for v8 Provider Runtime (Routing, Failover, Circuit Breaker, Cost Metrics)."""

import pytest

from zanything.providers import (
    ModelSpec,
    ProviderRequest,
    ProviderType,
)
from zanything.providers.circuit_breaker import CircuitBreaker, CircuitState
from zanything.providers.router import MockableProviderClient, ProviderRouter


def get_test_model_specs(provider: ProviderType) -> list[ModelSpec]:
    return [
        ModelSpec(
            model_id="default-model",
            provider=provider,
            input_cost_per_million=2.00,
            output_cost_per_million=8.00,
        )
    ]


@pytest.mark.anyio
async def test_successful_provider_routing_and_cost_calculation() -> None:
    """Verify provider generates response and calculates cost metrics."""
    router = ProviderRouter()
    openai_client = MockableProviderClient(
        provider_type=ProviderType.OPENAI,
        model_specs=get_test_model_specs(ProviderType.OPENAI),
        default_model="default-model",
    )
    router.register_provider(openai_client)

    req = ProviderRequest(
        messages=[{"role": "user", "content": "Hello, generate a strategy."}],
        tenant_id="tenant-acme",
    )
    resp = await router.execute_with_failover(req)

    assert resp.provider == ProviderType.OPENAI
    assert resp.prompt_tokens > 0
    assert resp.total_cost_usd > 0.0
    assert router.get_tenant_cost("tenant-acme") == resp.total_cost_usd


@pytest.mark.anyio
async def test_graceful_provider_failover() -> None:
    """Verify primary provider failure causes fallback to secondary provider."""
    router = ProviderRouter()

    # Primary provider: FAILING
    failing_openai = MockableProviderClient(
        provider_type=ProviderType.OPENAI,
        model_specs=get_test_model_specs(ProviderType.OPENAI),
        default_model="default-model",
        failing=True,
    )
    # Secondary provider: HEALTHY
    healthy_anthropic = MockableProviderClient(
        provider_type=ProviderType.ANTHROPIC,
        model_specs=get_test_model_specs(ProviderType.ANTHROPIC),
        default_model="default-model",
        failing=False,
    )

    router.register_provider(failing_openai)
    router.register_provider(healthy_anthropic)

    req = ProviderRequest(
        messages=[{"role": "user", "content": "Execute failover test."}],
        tenant_id="tenant-failover",
    )
    resp = await router.execute_with_failover(req)

    assert resp.provider == ProviderType.ANTHROPIC
    assert "anthropic" in resp.content.lower()


def test_circuit_breaker_state_transitions() -> None:
    """Verify circuit breaker opens after failure threshold and protects system."""
    cb = CircuitBreaker(
        name="test-cb", failure_threshold=2, recovery_timeout_seconds=0.1
    )
    assert cb.state == CircuitState.CLOSED
    assert cb.allow_request() is True

    # Record 1 failure -> still closed
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED

    # Record 2nd failure -> circuit OPENS
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.allow_request() is False

    # After recovery timeout -> circuit allows probe request (HALF_OPEN)
    import time

    time.sleep(0.15)
    assert cb.allow_request() is True
    assert cb.state == CircuitState.HALF_OPEN

    # Success in half open -> closes circuit
    cb.record_success()
    assert cb.state == CircuitState.CLOSED
