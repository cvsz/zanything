# zanything — Enterprise / Production Gold Master Checklist

This checklist is the repository-level release gate for calling `zanything` Enterprise-Grade Ready / Production-Grade Ready. The canonical execution ledger lives in `roadmap/exec-planning.md`; this file summarizes the final evidence gates.

## Installation & Lifecycle
- [ ] Clean installation from a supported fresh host is automated and proven.
- [ ] Upgrade from the previous supported release is proven.
- [ ] Rollback is proven.
- [ ] Repair/reinstall path is proven.
- [ ] Uninstall preserves or removes data according to documented policy.

## Identity, Authorization & Tenancy
- [ ] Production authentication is verified end-to-end.
- [ ] Cloudflare Access / OIDC trust boundary is explicit and validated.
- [ ] Forwarded identity headers are accepted only from a trusted proxy path.
- [ ] Anonymous fallback is disabled in production unless explicitly intended.
- [ ] RBAC/ABAC and deny-by-default authorization are verified.
- [ ] Tenant isolation is verified with cross-tenant negative tests.
- [ ] Service-account and break-glass paths are audited.

## Durable Runtime
- [ ] PostgreSQL-backed durable state is production-enabled.
- [ ] Queue/worker persistence and retry/DLQ behavior are production-enabled.
- [ ] Idempotency survives process restart where required.
- [ ] Migrations and rollback are tested.

## Secrets & Integrations
- [ ] Secrets are externalized and not committed to source or images.
- [ ] Secret rotation procedure is documented and tested.
- [ ] Integrations use least-privilege scopes, bounded timeouts, retries and idempotency.
- [ ] External side effects are audited and high-impact actions are confirmation-gated.

## Testing & Security
- [ ] Unit, integration, contract and E2E suites pass.
- [ ] Security regression suite passes.
- [ ] Load/soak/chaos tests meet release targets.
- [ ] Backup/restore, migration, rollback and upgrade tests pass.
- [ ] SAST/SCA/secret/container/IaC scans pass release policy.
- [ ] No unresolved Critical/High findings remain without formal risk treatment.
- [ ] SBOM and provenance are generated.
- [ ] Release artifacts are checksummed/signed where supported.

## Observability & Reliability
- [ ] Structured logs, metrics and traces are operational.
- [ ] SLOs/error budgets are defined.
- [ ] Alerts are actionable and tested.
- [ ] Failure/degraded modes are tested.
- [ ] Capacity target is validated.

## Backup / DR / Privacy
- [ ] Backups are encrypted and off-host where appropriate.
- [ ] Restore has been tested.
- [ ] RPO/RTO are defined and DR procedure is proven.
- [ ] Retention, deletion, export, redaction and privacy controls are validated.

## Operations & Release
- [ ] Incident, upgrade, rollback, backup and DR runbooks are complete.
- [ ] API compatibility and migration notes are complete.
- [ ] Admin/operator/user documentation is complete.
- [ ] Production Readiness Review is approved.
- [ ] Gold Master release evidence is archived.

## Current repository note
The roadmap currently records v5–v66 as complete. This checklist should be checked only against current release evidence, not milestone labels alone. In particular, production auth must not trust arbitrary client-supplied forwarding headers unless the deployment guarantees that only a trusted reverse proxy can set them.
