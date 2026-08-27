"""Tests for v9-v12 Platform Core Services (Integrations, Secrets, Policy Engine)."""

import pytest

from zanything.adapters import AdapterCategory, GitHubAdapter, IntegrationContext
from zanything.auth import Principal, Role
from zanything.policy import ActionClass, PolicyEngine
from zanything.secrets import EnvSecretProvider, SecretRedactor


@pytest.mark.anyio
async def test_github_adapter_execution() -> None:
    """Verify GitHub integration adapter executes create_issue action."""
    adapter = GitHubAdapter()
    assert adapter.category == AdapterCategory.CODE_VCS
    assert await adapter.check_health() is True

    ctx = IntegrationContext(
        tenant_id="tenant-vcs", actor_id="alice", request_id="req-vcs-1"
    )
    result = await adapter.execute(
        action="create_issue",
        params={"repo": "cvsz/zanything", "title": "Fix security vulnerability"},
        context=ctx,
    )
    assert result.success is True
    assert "issue_id" in result.data
    assert result.data["issue_id"] == 101


def test_secret_redaction() -> None:
    """Verify sensitive keys and tokens are redacted from log strings."""
    raw_log = (
        "Error with authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 "
        "and API-KEY: ghp_1234567890abcdef1234567890abcdef1234"
    )
    redacted = SecretRedactor.redact(raw_log)
    assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in redacted
    assert "ghp_1234567890abcdef1234567890abcdef1234" not in redacted
    assert "[REDACTED]" in redacted


def test_env_secret_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify environment secret provider resolves values."""
    monkeypatch.setenv("ZANYTHING_CUSTOM_SECRET", "super-secret-token")
    provider = EnvSecretProvider(prefix="ZANYTHING_")
    assert provider.get_secret("CUSTOM_SECRET") == "super-secret-token"
    assert provider.get_secret("env://CUSTOM_SECRET") == "super-secret-token"


def test_policy_classification_and_evaluation() -> None:
    """Verify action risk classification and confirmation requirements."""
    engine = PolicyEngine()

    assert engine.classify_action("fetch_task_status") == ActionClass.READ_ONLY
    assert engine.classify_action("create_task_draft") == ActionClass.REVERSIBLE_WRITE
    assert (
        engine.classify_action("deploy_production_cluster") == ActionClass.HIGH_IMPACT
    )

    operator = Principal(subject="bob", roles=[Role.OPERATOR], tenant_id="t1")
    decision = engine.evaluate(operator, "deploy_production_cluster")
    assert decision.action_class == ActionClass.HIGH_IMPACT
    assert decision.requires_approval is True
