# zanything Implementation Checklist

This checklist tracks repository/project foundations that must remain synchronized with the canonical implementation ledger in `exec-planning.md`.

## Repository identity
- [x] Repository name and project description aligned to `zanything`.
- [x] Canonical README points to implementation prompts and Gold Master roadmap.
- [ ] Confirm repository topics, description, homepage, and public metadata match the enterprise operator scope.

## Governance
- [ ] Review `.github/CODEOWNERS` for current ownership.
- [x] Contribution and code-of-conduct documents exist.
- [ ] Confirm branch protection/rulesets require appropriate pull request and status checks.
- [ ] Confirm required reviews/approvals for protected production changes.

## Security
- [x] `SECURITY.md` exists.
- [x] CodeQL workflow exists.
- [x] Dependency Review workflow exists.
- [x] Dependabot configuration exists.
- [x] CI performs a basic tracked-secret filename guard.
- [ ] Confirm secret scanning/push protection repository settings where available.
- [ ] Add stack-specific SAST/SCA/container/IaC/SBOM gates as implementation becomes real.
- [ ] Keep Actions permissions least-privilege.

## Project execution
- [x] `exec-planning.md` is the canonical bounded implementation ledger.
- [x] `ROADMAP-TO-GOLD-MASTER.md` tracks v5 → v66 milestones.
- [x] `GOLD-MASTER-CHECKLIST.md` defines final enterprise/production exit gates.
- [x] `prompts/MASTER-IMPLEMENTATION.prompt.md` defines the implementation contract.
- [x] Phase implementation prompts exist for v5 → v66.
- [x] Specialist implementation prompts exist for all universal capability groups.
- [ ] Execute v5 onward in dependency order with evidence-backed completion.

## CI/CD
- [x] Baseline CI workflow exists.
- [x] CodeQL workflow exists.
- [x] Dependency Review workflow exists.
- [ ] CI must run successfully on the active implementation PR before merge.
- [ ] Add real build/test/package jobs as implementation code lands.
- [ ] Add deployment environments, approvals and release protections before production deployment.

## Release
- [ ] Confirm semantic versioning/release policy.
- [ ] Synchronize `CHANGELOG.md` with implementation releases.
- [ ] Add SBOM/provenance/signing/attestation gates before Gold Master.
- [ ] Prove install, upgrade, backup/restore and rollback before production-ready claims.

## Documentation
- [x] README is aligned to zanything.
- [x] Roadmap is aligned to enterprise implementation.
- [ ] Keep `ARCHITECTURE.md`, `DEPLOYMENT.md`, `SECURITY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, GitHub templates and runbooks synchronized with implementation changes.
- [ ] Add operator/admin/user/API/integration documentation as the corresponding runtime is implemented.

## Merge readiness
- [ ] Branch is current with `main` and conflict-free.
- [ ] Required CI/security workflows actually ran and are green.
- [ ] Review threads are resolved.
- [ ] Documentation and project ledgers match the proposed change.
- [ ] No unsupported production-ready claim is introduced.

## Final Gold Master verification
- [ ] Fresh clean install proven.
- [ ] Production identity/tenant/RBAC proven.
- [ ] Durable DB/queue and secret management proven.
- [ ] Security/reliability/eval/test gates pass.
- [ ] Observability/SLOs operational.
- [ ] Backup/restore/DR proven.
- [ ] Upgrade/rollback proven.
- [ ] Gold Master evidence archived.
