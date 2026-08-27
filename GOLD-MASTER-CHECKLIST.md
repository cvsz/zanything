# Production / Enterprise Gold Master Exit Criteria

A release may be called **Production-Grade Ready / Enterprise-Grade Ready** only when all applicable gates are evidenced.

- [ ] Clean installation from a supported fresh host is automated and proven.
- [ ] Upgrade from the previous supported release is proven.
- [ ] Rollback is proven.
- [ ] Production authentication and tenant isolation are verified.
- [ ] RBAC/ABAC and deny-by-default authorization are verified.
- [ ] Durable database and queue runtimes are production-backed.
- [ ] Secrets are externalized and rotation is documented/tested.
- [ ] Integrations use scoped credentials, timeouts, retries, idempotency and audit.
- [ ] Unit/integration/contract/E2E/security/load/chaos tests pass.
- [ ] CI/CD release gates pass.
- [ ] SAST/SCA/secret/container/IaC scans pass policy.
- [ ] No unresolved Critical/High security findings accepted without formal risk treatment.
- [ ] SBOM and provenance are generated.
- [ ] Release artifacts are checksummed/signed where supported.
- [ ] OpenTelemetry/logging/metrics/tracing and actionable alerts are operational.
- [ ] SLOs and error budgets are defined.
- [ ] Backups are encrypted and restore has been tested.
- [ ] RPO/RTO and disaster-recovery procedures are proven.
- [ ] Load/capacity testing meets target.
- [ ] Failure/degraded modes are tested.
- [ ] Data retention/privacy/deletion/export controls are validated.
- [ ] Incident, upgrade, rollback, backup and DR runbooks are complete.
- [ ] API compatibility and migration notes are complete.
- [ ] Admin/operator/user documentation is complete.
- [ ] Production Readiness Review is approved.
- [ ] Gold Master release evidence is archived.
