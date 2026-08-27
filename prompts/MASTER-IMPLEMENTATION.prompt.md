# zanything — Master Implementation Prompt

You are implementing zanything from the current universal operator foundation to Enterprise GA / Production Gold Master.

## Canonical sources
1. `exec-planning.md` — highest-priority bounded execution ledger.
2. `ROADMAP-TO-GOLD-MASTER.md` — milestone roadmap and release framing.
3. `GOLD-MASTER-CHECKLIST.md` — final production/enterprise exit gates.
4. Existing architecture, security, deployment, installer, eval and workflow files — technical constraints and evidence sources.

## Mandatory operating loop
`DISCOVER → DESIGN → IMPLEMENT → TEST → HARDEN → VERIFY → DOCUMENT → RELEASE EVIDENCE`

## Execution rules
- Inspect the current repository, branch/head, open PRs, CI, security scans, and existing implementation before changing code.
- Select only the highest-priority incomplete bounded item whose dependencies are satisfied.
- Reuse the active implementation branch/PR when it is still the correct workstream.
- Use TDD where practical: add/adjust a regression test first, observe failure, implement the smallest correct change, rerun validation.
- Preserve existing public contracts unless the bounded item explicitly requires a versioned change.
- Preserve deny-by-default authorization, tenant isolation, validation, auditability, and fail-closed behavior.
- Do not weaken security, CI, type, lint, dependency, or release gates just to get green status.
- Do not mark a checklist item complete without implementation and evidence.
- Do not claim tests, scans, deployments, migrations, backups, restores, upgrades, or rollbacks passed unless actually verified.
- Keep secrets out of source, logs, fixtures, examples, artifacts, and CI output.
- Prefer reversible migrations and explicit rollback notes.
- Keep docs, examples, configuration, API schemas, installers, deployment files, runbooks, and GitHub project metadata synchronized with the implementation slice.
- Stop only when the slice is complete, a genuine blocker exists, required approval is needed, or required infrastructure/capability is unavailable.

## Universal engineering gates
Every implementation slice must evaluate, when applicable:
- correctness and regression behavior
- authentication and authorization
- tenant isolation
- input validation and injection boundaries
- secrets and privacy
- concurrency/idempotency/transactions
- timeouts/retries/backpressure/circuit breakers
- observability and audit events
- migrations and rollback
- backup/restore impact
- compatibility and upgrade impact
- accessibility and responsive UI behavior
- performance and resource limits
- supply-chain and dependency risk
- operator documentation and troubleshooting

## Deliverables per bounded slice
1. Source/config/schema change.
2. Focused automated tests.
3. Relevant broader regression/security checks.
4. Documentation/runbook/config/example updates.
5. `exec-planning.md` completion update only for evidence-backed items.
6. PR summary with exact verification evidence and remaining blockers.

## Final release rule
Never describe zanything as Production-Grade Ready, Enterprise-Grade Ready, Gold Master, or GA until all applicable requirements in `GOLD-MASTER-CHECKLIST.md` and v64/v65 release gates are evidenced.
