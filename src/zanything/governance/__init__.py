"""Phase C: Reliability, SLO, Chaos, and Compliance runtime."""

import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.governance")


class SLOStatus(StrEnum):
    """Service Level Objective health state."""

    HEALTHY = "healthy"
    WARNING = "warning"
    BREACHED = "breached"


class SLOMetric(BaseModel):
    """Real-time Service Level Indicator and Error Budget calculation."""

    name: str
    target_pct: float = 99.9
    actual_pct: float
    error_budget_remaining_pct: float
    status: SLOStatus
    window_hours: int = 24


class SLOMonitor:
    """Calculates availability, latency, and error budgets."""

    def evaluate_availability(
        self, total_requests: int, failed_requests: int, target_pct: float = 99.9
    ) -> SLOMetric:
        if total_requests == 0:
            return SLOMetric(
                name="Availability",
                target_pct=target_pct,
                actual_pct=100.0,
                error_budget_remaining_pct=100.0,
                status=SLOStatus.HEALTHY,
            )

        success_requests = total_requests - failed_requests
        actual_pct = round((success_requests / total_requests) * 100, 3)

        allowed_failure_pct = 100.0 - target_pct
        actual_failure_pct = (failed_requests / total_requests) * 100.0
        budget_used = (
            actual_failure_pct / allowed_failure_pct if allowed_failure_pct > 0 else 1.0
        )
        budget_remaining = max(0.0, round((1.0 - budget_used) * 100, 2))

        status = SLOStatus.HEALTHY
        if actual_pct < target_pct:
            status = SLOStatus.BREACHED
        elif budget_remaining < 20.0:
            status = SLOStatus.WARNING

        return SLOMetric(
            name="Availability",
            target_pct=target_pct,
            actual_pct=actual_pct,
            error_budget_remaining_pct=budget_remaining,
            status=status,
        )


class ChaosHarness:
    """Injects faults, latency, and network partitions to verify resilience."""

    def __init__(self) -> None:
        self._faults_active: set[str] = set()

    def inject_fault(self, fault_type: str) -> None:
        self._faults_active.add(fault_type)
        logger.warning(f"Chaos harness injected fault: {fault_type}")

    def clear_fault(self, fault_type: str) -> None:
        self._faults_active.discard(fault_type)
        logger.info(f"Chaos harness cleared fault: {fault_type}")

    def should_fail(self, fault_type: str) -> bool:
        return fault_type in self._faults_active


class AuditEvidenceBundle(BaseModel):
    """Tamper-evident compliance & forensic evidence export."""

    tenant_id: str
    bundle_id: str
    exported_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    total_events: int
    events_hash: str
    compliance_standard: str = "SOC2-Type-II / ISO-27001"
    metadata: dict[str, Any] = Field(default_factory=dict)
