# Architecture / Security / DevOps-SRE Implementation Prompt

Implement production Architecture, Security, and DevOps/SRE capabilities for zanything.

## Architecture
- Model system boundaries, data ownership, APIs/events, state transitions, trust zones, and failure modes.
- Produce ADRs and migration/rollback plans for material design choices.
- Define scalability and compatibility assumptions explicitly.
- Prefer simpler architecture unless distribution is justified by measurable requirements.

## Security
- Threat-model authentication, authorization, tenant isolation, input boundaries, secrets, filesystem/network egress, SSRF, injection, XSS/CSRF, unsafe deserialization, dependency/supply-chain risk, rate limits, auditability, and least privilege.
- Deny by default and fail closed.
- Calibrate severity from exploitability and impact evidence.
- Never weaken a gate to make CI pass.

## DevOps/SRE
- Reproducible containers/builds.
- Environment-specific configuration without secret sprawl.
- Health/readiness/liveness, graceful shutdown, resource limits.
- Safe migrations, rolling/canary deployment and rollback.
- Structured logs, metrics, traces, dashboards and SLOs.
- Backup/restore and DR evidence.
- Kubernetes/Helm/IaC validation where applicable.

## Tests and evidence
- architecture contract tests
- auth/tenant boundary tests
- security regressions
- container/IaC scans
- deploy/rollback smoke tests
- migration tests
- degraded-mode tests
- readiness and failure-mode tests
- operational runbooks

Do not mark complete without implementation, tests, hardening, observability and release evidence.
