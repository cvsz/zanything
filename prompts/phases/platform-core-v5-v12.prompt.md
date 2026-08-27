# Phase Prompt — v5–v12 Platform Core

Implement the Platform Core in bounded sequence. Do not skip dependencies or mark future slices complete without evidence.

## v5 Identity & Access
Production OIDC/JWT, SSO, service accounts, tenant-aware principals, RBAC/ABAC, role-management UI/API, access-review/break-glass procedures and integration tests.

## v6 Durable Data
PostgreSQL repositories, migrations/versioning, tenant-scoped queries, transactions/concurrency, persistent idempotency/audit, retention, backup/restore and rollback tests.

## v7 Queue & Workers
Durable queue abstraction with Redis reference backend, retries/backoff/DLQ, cancellation, priorities, resumability, heartbeats, saturation/backpressure and chaos/recovery tests.

## v8 Provider Runtime
Capability contract, registry/routing, timeouts/rate limits/circuit breakers, fallback/degraded mode, cost metrics, health/admin UI and contract tests.

## v9 Integration Fabric
Universal adapter contract and production-safe GitHub/GitLab, Slack/Teams, Google/Microsoft, Jira/Linear/Notion, DB/storage/internal API adapters with scoped credentials, idempotency and audit.

## v10 Secrets
Secret provider abstraction, environment/dev reference, Vault/KMS/cloud adapters, references instead of raw persistence, rotation/audit, redaction tests.

## v11 Policy & Confirmation
Action classes, policy-as-code, approval state machine, dry-run/simulation, optional dual control, approval inbox, bypass regressions.

## v12 Enterprise Admin GUI
Tenants/users/roles, tasks/projects, providers/integrations, policies/approvals, audit, cost/quota, queue/workers, health/incident views with responsive/accessibility/E2E coverage.

## Exit gate
All core services must be tenant-safe, auditable, observable, migratable, recoverable, documented and verified before Phase B begins.
