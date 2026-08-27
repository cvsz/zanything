# Phase Prompt — v41–v55 Platform Engineering & Distribution

Implement production platform engineering, distribution and lifecycle management.

## Scope
- v41 API Productionization
- v42 Webhook/Event Platform
- v43 Plugin/Extension SDK
- v44 Multi-Region Readiness
- v45 HA & Zero-Downtime
- v46 Kubernetes Production Profile
- v47 Terraform/IaC
- v48 Automated Installer 2.0
- v49 Configuration Wizard
- v50 Upgrade Manager
- v51 Health & Readiness Center
- v52 Test Matrix
- v53 Acceptance/Eval Framework
- v54 Red-Team & Abuse Testing
- v55 Installer Validation Matrix

## Requirements
- Versioned APIs, stable error contracts, pagination, rate limits, idempotency and generated SDKs.
- Signed webhooks, delivery logs, retries, replay, dedupe and event versioning.
- Versioned provider/integration/specialist SDKs and compatibility policy.
- Regional routing/failover/data-residency strategy.
- API/worker/data-store HA and zero-downtime deployment/migration evidence.
- Kubernetes ingress/TLS/external secrets/PodSecurity/network policies/HPA/PDB/topology configuration.
- Terraform modules, remote state and policy/drift detection.
- Automated install/repair/upgrade/rollback/uninstall across supported profiles, including offline where required.
- Configuration wizard with validation-before-save and secret-reference handling.
- Upgrade compatibility, backup-before-upgrade, canary and rollback verification.
- Dependency health center and degraded-mode visibility.
- Full unit/integration/contract/E2E/UI/accessibility/security/load/chaos/backup/migration/rollback/upgrade test matrix.
- Specialist and anti-hallucination evals.
- Prompt injection, tool abuse, tenant escape and data-exfiltration red-team tests.
- Clean-host installer validation across the declared supported OS matrix.

## Exit gate
Distribution is complete only when a supported clean environment can install, configure, verify, upgrade, rollback and uninstall the system reproducibly with evidence.
