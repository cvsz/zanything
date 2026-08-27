"""DevOps & SRE Engine: Deployment planning and Rollback gates."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.engines.devops")


class DeploymentTarget(StrEnum):
    """Target deployment infrastructure."""

    KUBERNETES = "kubernetes"
    HELM = "helm"
    ARGOCD = "argocd"
    TERRAFORM = "terraform"
    ANSIBLE = "ansible"
    DOCKER_COMPOSE = "docker_compose"
    AWS_ECS = "aws_ecs"
    GCP_CLOUDRUN = "gcp_cloudrun"
    AZURE_CONTAINER_APPS = "azure_container_apps"
    CLOUDFLARE_WORKERS = "cloudflare_workers"
    NOMAD = "nomad"
    SERVERLESS = "serverless"
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

        target_steps_map: dict[DeploymentTarget, list[str]] = {
            DeploymentTarget.KUBERNETES: [
                "Run preflight k8s cluster capacity and quota checks",
                f"Pull image zanything:{app_version}",
                "Deploy candidate pods with RollingUpdate strategy",
                "Execute readiness probe on /readyz (initialDelay=5s, period=10s)",
                "Shift Service and Ingress traffic from active to candidate",
            ],
            DeploymentTarget.HELM: [
                "Lint Helm chart templates and validate values.yaml schema",
                f"Deploy Helm release zanything-prod --set image.tag={app_version}",
                "Wait for Deployment rollout status completion (timeout=300s)",
                "Execute Helm post-upgrade test hooks",
            ],
            DeploymentTarget.ARGOCD: [
                "Commit and push declarative GitOps manifests to repository",
                "Trigger ArgoCD Application sync for 'zanything-prod'",
                "Monitor Health Status transitions (Progressing -> Healthy)",
                "Verify automated progressive delivery canary metrics",
            ],
            DeploymentTarget.TERRAFORM: [
                "Initialize remote state and execute 'terraform validate'",
                f"Generate Terraform plan with var.app_version={app_version}",
                "Enforce OPA / Sentinel policy compliance checks",
                "Apply infrastructure state changes with state locking",
            ],
            DeploymentTarget.ANSIBLE: [
                "Run Ansible dry-run syntax check (--check mode)",
                f"Execute playbook site.yml with extra-vars 'version={app_version}'",
                "Perform rolling host restart with serial execution (batch 20%)",
                "Verify systemd service and HTTP health across all inventory nodes",
            ],
            DeploymentTarget.DOCKER_COMPOSE: [
                "Validate compose.yaml syntax and environment variables",
                f"Pull new container images with tag {app_version}",
                "Start new services with 'docker compose up -d --no-deps --build'",
                "Prune orphaned containers and verify port bindings",
            ],
            DeploymentTarget.AWS_ECS: [
                f"Register new ECS Task Definition with image tag {app_version}",
                "Update ECS Service with CodeDeploy Blue/Green deployment controller",
                "Route 10% test traffic to Green Target Group for 5 minutes",
                "Shift 100% production traffic to Green Target Group upon health pass",
            ],
            DeploymentTarget.GCP_CLOUDRUN: [
                f"Deploy new revision to Google Cloud Run with tag {app_version}",
                "Route 0% traffic to candidate revision and run smoke tests",
                "Gradually migrate traffic with traffic split (10% -> 50% -> 100%)",
            ],
            DeploymentTarget.AZURE_CONTAINER_APPS: [
                f"Deploy new revision to Azure Container Apps with tag {app_version}",
                "Verify readiness probe on candidate revision endpoint",
                "Switch active revision traffic weighting to 100%",
            ],
            DeploymentTarget.CLOUDFLARE_WORKERS: [
                "Compile and bundle edge worker script with Wrangler",
                f"Deploy Cloudflare Worker version {app_version} with gradual rollout",
                "Verify zero-latency edge distribution and Worker analytics",
            ],
            DeploymentTarget.NOMAD: [
                "Validate Nomad job specification syntax",
                f"Submit Nomad job dispatch with artifact version {app_version}",
                "Monitor Nomad task group allocation and canary healthy status",
                "Promote Nomad canary allocation to active production",
            ],
            DeploymentTarget.SERVERLESS: [
                "Package serverless bundle with Serverless Framework / AWS SAM",
                f"Deploy Lambda function version {app_version} with alias 'live'",
                "Execute CodeDeploy canary deployment with Lambda warmers",
            ],
            DeploymentTarget.SYSTEMD: [
                f"Deploy binary / package zanything v{app_version} to /usr/local/bin",
                "Reload systemd daemon with 'systemctl daemon-reload'",
                "Restart service with 'systemctl restart zanything.service'",
                "Verify service active status with 'systemctl is-active zanything'",
            ],
        }

        steps = target_steps_map.get(
            target,
            [
                "Run preflight resource checks",
                f"Deploy release zanything:{app_version}",
                "Execute readiness probe on /readyz",
                "Shift traffic to candidate",
            ],
        )

        rollback = [
            f"Trigger automated rollback to previous stable release for {target.value}",
            "Revert traffic routing and DNS/Ingress records",
            "Capture diagnostics dump and alert SRE on-call via PagerDuty / Slack",
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
