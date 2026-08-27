"""DevOps & SRE Engine: Deployment planning and Rollback gates."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.engines.devops")


class DeploymentTarget(StrEnum):
    """Target deployment infrastructure."""

    DOCKER_COMPOSE = "docker_compose"
    KUBERNETES = "kubernetes"
    HELM = "helm"
    SYSTEMD = "systemd"


class DeploymentPlan(BaseModel):
    """Execution plan for infrastructure provisioning or application deployment."""

    plan_id: str
    target: DeploymentTarget
    tenant_id: str
    steps: list[str]
    health_probes: list[str]
    rollback_steps: list[str]
    requires_approval: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)


class DevOpsEngine:
    """Plans zero-downtime deployments, health checks, and rollbacks."""

    def plan_deployment(
        self, target: DeploymentTarget, tenant_id: str, app_version: str
    ) -> DeploymentPlan:
        """Create gated deployment plan with health checks and automated rollback."""
        logger.info(
            f"Generating deployment plan for target '{target.value}' (v{app_version})"
        )

        steps = [
            "Run preflight resource checks",
            f"Pull image zanything:{app_version}",
            "Deploy candidate pods / containers",
            "Execute readiness probe on /readyz",
            "Shift traffic from active to candidate",
        ]
        rollback = [
            "Roll back ingress routing to previous replica",
            "Terminate failing candidate pods",
            "Capture diagnostics dump and alert SRE on-call",
        ]

        return DeploymentPlan(
            plan_id=f"deploy-{target.value}-{app_version}",
            target=target,
            tenant_id=tenant_id,
            steps=steps,
            health_probes=["/healthz", "/readyz"],
            rollback_steps=rollback,
            requires_approval=True,
        )
