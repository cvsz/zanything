"""Security Engine: Threat modeling and Vulnerability scanning."""

from enum import StrEnum

from pydantic import BaseModel

from zanything.logging import get_logger

logger = get_logger("zanything.engines.security")


class Severity(StrEnum):
    """Vulnerability severity ratings."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityFinding(BaseModel):
    """Identified security risk or architectural flaw."""

    check_id: str
    title: str
    severity: Severity
    description: str
    recommendation: str
    affected_component: str


class SecurityAuditReport(BaseModel):
    """Formal security audit and threat model report."""

    target_service: str
    tenant_id: str
    passed: bool
    findings: list[SecurityFinding]
    critical_count: int = 0
    high_count: int = 0


class SecurityEngine:
    """Performs trust-boundary reviews and threat modeling evaluation."""

    def audit_configuration(
        self, target_service: str, tenant_id: str, checks: list[dict[str, str]]
    ) -> SecurityAuditReport:
        """Run automated security baseline checks against configuration."""
        findings: list[SecurityFinding] = []

        for chk in checks:
            if chk.get("allow_anonymous") == "true" and chk.get("env") == "production":
                findings.append(
                    SecurityFinding(
                        check_id="SEC-001",
                        title="Anonymous Access Enabled in Production",
                        severity=Severity.HIGH,
                        description="allow_anonymous=True is set for production.",
                        recommendation="Enforce mandatory OIDC/JWT Bearer auth.",
                        affected_component="auth/dependencies.py",
                    )
                )

        crit_count = sum(1 for f in findings if f.severity == Severity.CRITICAL)
        high_count = sum(1 for f in findings if f.severity == Severity.HIGH)
        passed = (crit_count == 0) and (high_count == 0)

        logger.info(
            f"Security audit on '{target_service}' completed: "
            f"Passed={passed} (Critical: {crit_count}, High: {high_count})"
        )

        return SecurityAuditReport(
            target_service=target_service,
            tenant_id=tenant_id,
            passed=passed,
            findings=findings,
            critical_count=crit_count,
            high_count=high_count,
        )
