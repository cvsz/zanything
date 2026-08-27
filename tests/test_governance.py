"""Integration test suite for Phase C (Reliability, SLO, Chaos, Compliance)."""

from zanything.governance import (
    AuditEvidenceBundle,
    ChaosHarness,
    SLOMonitor,
    SLOStatus,
)


def test_slo_monitor_availability_and_error_budget() -> None:
    """Verify SLO monitor tracks SLA targets and error budget exhaustion."""
    monitor = SLOMonitor()

    # 10,000 requests with 5 failures -> 99.95% availability (Target 99.9%) -> HEALTHY
    slo_healthy = monitor.evaluate_availability(
        total_requests=10000, failed_requests=5, target_pct=99.9
    )
    assert slo_healthy.status == SLOStatus.HEALTHY
    assert slo_healthy.actual_pct == 99.95
    assert slo_healthy.error_budget_remaining_pct == 50.0

    # 10,000 requests with 20 failures -> 99.80% availability -> BREACHED
    slo_breached = monitor.evaluate_availability(
        total_requests=10000, failed_requests=20, target_pct=99.9
    )
    assert slo_breached.status == SLOStatus.BREACHED
    assert slo_breached.actual_pct == 99.80
    assert slo_breached.error_budget_remaining_pct == 0.0


def test_chaos_fault_injection_harness() -> None:
    """Verify chaos harness activates, checks, and clears injected faults."""
    chaos = ChaosHarness()
    assert chaos.should_fail("redis_timeout") is False

    chaos.inject_fault("redis_timeout")
    assert chaos.should_fail("redis_timeout") is True

    chaos.clear_fault("redis_timeout")
    assert chaos.should_fail("redis_timeout") is False


def test_audit_evidence_bundle() -> None:
    """Verify compliance forensic bundle creation with standard attestation."""
    bundle = AuditEvidenceBundle(
        tenant_id="tenant-fintech",
        bundle_id="bundle-q3-2026",
        total_events=1542,
        events_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )
    assert bundle.total_events == 1542
    assert "SOC2" in bundle.compliance_standard
