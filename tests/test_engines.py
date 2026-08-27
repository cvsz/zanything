"""Integration tests for Phase B Runtime (Artifacts, Research, Coding, DevOps)."""

import pytest

from zanything.artifacts import MemoryArtifactStorage
from zanything.engines.coding import CodingEngine, TestExecutionResult
from zanything.engines.devops import DeploymentTarget, DevOpsEngine
from zanything.engines.research import DeepResearchEngine, ResearchSource
from zanything.engines.security import SecurityEngine, Severity


@pytest.mark.anyio
async def test_artifact_storage_and_provenance() -> None:
    """Verify storing artifacts computes SHA256 and retrieves with tenant isolation."""
    storage = MemoryArtifactStorage()
    content = b"Enterprise Universal AI Operator Build Artifact"
    meta = await storage.store(
        tenant_id="tenant-build-1",
        filename="report.pdf",
        content=content,
        content_type="application/pdf",
        task_id="task-build-99",
    )

    assert meta.filename == "report.pdf"
    assert meta.size_bytes == len(content)
    assert len(meta.sha256) == 64
    assert meta.provenance_task_id == "task-build-99"

    # Retrieve in same tenant
    retrieved = await storage.retrieve("tenant-build-1", meta.artifact_id)
    assert retrieved == content

    # Other tenant cannot access
    assert await storage.retrieve("tenant-other", meta.artifact_id) is None


def test_deep_research_synthesis() -> None:
    """Verify research engine ranks sources by authority and outputs findings."""
    engine = DeepResearchEngine()
    sources = [
        ResearchSource(
            url="https://sec.gov/filing/123",
            title="SEC 10-K Report",
            authority_score=0.95,
            freshness_score=0.90,
            is_primary=True,
            excerpt="Financial reserves audited.",
        ),
        ResearchSource(
            url="https://blog.example.com/opinion",
            title="Blog Opinion",
            authority_score=0.40,
            freshness_score=0.80,
            is_primary=False,
            excerpt="Speculative commentary.",
        ),
    ]

    report = engine.analyze_and_synthesize(
        "Corporate Reserves", sources, "tenant-audit"
    )
    assert report.topic == "Corporate Reserves"
    assert report.overall_confidence > 0.60
    assert len(report.findings) == 1
    assert "https://sec.gov/filing/123" in report.findings[0].sources


def test_coding_patch_evaluation() -> None:
    """Verify coding engine validates patches against test execution metrics."""
    engine = CodingEngine()
    test_result = TestExecutionResult(
        passed=True,
        total_tests=33,
        passed_tests=33,
        failed_tests=0,
        duration_seconds=2.5,
        output_log="33 passed in 2.5s",
    )

    patch = engine.evaluate_patch("diff --git a/app.py b/app.py", test_result)
    assert patch.verified is True
    assert patch.tests_passed is True


def test_security_audit_engine() -> None:
    """Verify security engine detects high-risk configurations."""
    engine = SecurityEngine()
    checks = [{"allow_anonymous": "true", "env": "production"}]

    report = engine.audit_configuration("zanything-api", "tenant-prod", checks)
    assert report.passed is False
    assert report.high_count == 1
    assert report.findings[0].severity == Severity.HIGH
    assert report.findings[0].check_id == "SEC-001"


def test_devops_deployment_planning() -> None:
    """Verify DevOps engine produces gated deployment plan with rollback."""
    engine = DevOpsEngine()
    plan = engine.plan_deployment(DeploymentTarget.KUBERNETES, "tenant-prod", "0.1.0")

    assert plan.target == DeploymentTarget.KUBERNETES
    assert plan.requires_approval is True
    assert len(plan.steps) > 0
    assert len(plan.rollback_steps) > 0
    assert "/readyz" in plan.health_probes
