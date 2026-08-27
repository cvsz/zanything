"""Integration tests for Phase D & E (Entitlement, Diagnostics, GA Gate)."""

from zanything.distribution import (
    DiagnosticBundle,
    EntitlementPolicy,
    FeatureTier,
    GoldMasterReleaseGate,
)


def test_entitlement_policy() -> None:
    """Verify enterprise entitlement tier allows full provider access."""
    policy = EntitlementPolicy(tier=FeatureTier.ENTERPRISE)
    assert policy.max_concurrent_workers == 50
    assert "openai" in policy.allowed_providers
    assert "gemini" in policy.allowed_providers
    assert policy.audit_export_enabled is True


def test_support_diagnostic_bundle() -> None:
    """Verify diagnostic bundle captures health snapshots without leaking secrets."""
    diag = DiagnosticBundle(
        bundle_id="diag-2026-08-27",
        tenant_id="tenant-core",
        system_health={"api": "healthy", "db": "healthy", "queue": "healthy"},
        active_workers=8,
        open_circuits=[],
    )
    assert diag.bundle_id == "diag-2026-08-27"
    assert diag.system_health["db"] == "healthy"
    assert diag.active_workers == 8


def test_gold_master_release_gate_evaluation() -> None:
    """Verify Gold Master release gate requires all criteria before GA approval."""
    # Incomplete criteria -> blocked
    gate_blocked = GoldMasterReleaseGate(
        version="1.0.0-GA",
        all_tests_green=True,
        security_clean=False,  # Unresolved issue
        sbom_generated=True,
        dr_drill_verified=True,
        sign_off_operator="cvsz",
    )
    assert gate_blocked.evaluate() is False
    assert gate_blocked.passed_release_gate is False

    # Complete green criteria -> approved
    gate_approved = GoldMasterReleaseGate(
        version="1.0.0-GA",
        all_tests_green=True,
        security_clean=True,
        sbom_generated=True,
        dr_drill_verified=True,
        sign_off_operator="cvsz",
    )
    assert gate_approved.evaluate() is True
    assert gate_approved.passed_release_gate is True
