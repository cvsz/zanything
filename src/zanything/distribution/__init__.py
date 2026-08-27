"""Phase D & E: Distribution, Entitlement, and GA Release Gates."""

import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.distribution")


class FeatureTier(StrEnum):
    """Enterprise licensing and entitlement tiers."""

    COMMUNITY = "community"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class EntitlementPolicy(BaseModel):
    """Tenant feature entitlement and quota constraints."""

    tier: FeatureTier = FeatureTier.ENTERPRISE
    max_concurrent_workers: int = 50
    allowed_providers: list[str] = Field(
        default_factory=lambda: ["openai", "anthropic", "gemini", "vertex", "local"]
    )
    airgapped_mode_enabled: bool = False
    audit_export_enabled: bool = True


class DiagnosticBundle(BaseModel):
    """System diagnostic dump for enterprise support and incident triage."""

    bundle_id: str
    tenant_id: str
    generated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
    system_health: dict[str, str]
    active_workers: int
    open_circuits: list[str] = Field(default_factory=list)
    sanitized_config: dict[str, Any] = Field(default_factory=dict)


class GoldMasterReleaseGate(BaseModel):
    """Formal sign-off gating release of Enterprise GA Gold Master."""

    version: str
    all_tests_green: bool
    security_clean: bool
    sbom_generated: bool
    dr_drill_verified: bool
    passed_release_gate: bool = False
    sign_off_operator: str

    def evaluate(self) -> bool:
        self.passed_release_gate = (
            self.all_tests_green
            and self.security_clean
            and self.sbom_generated
            and self.dr_drill_verified
        )
        if self.passed_release_gate:
            logger.info(
                f"Gold Master GA gate PASSED for v{self.version} "
                f"by {self.sign_off_operator}"
            )
        else:
            logger.warning(
                f"Gold Master GA gate BLOCKED for v{self.version} "
                f"by {self.sign_off_operator}"
            )
        return self.passed_release_gate
