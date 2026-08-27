# zanything — Anything Enterprise Universal Operator

zanything is the implementation repository for a universal enterprise AI operator spanning Research, Deep Research, Coding, Debugging, Architecture, Security, DevOps/SRE, Data, Documents, Spreadsheets, Presentations, Images, Movie Posters, UI/UX, Marketing, Business, Automation, Decision Making, Multimodal workflows, and end-to-end Project Execution.

## Canonical implementation entry points

1. `prompts/MASTER-IMPLEMENTATION.prompt.md` — master implementation contract.
2. `exec-planning.md` — v5 → v66 canonical execution ledger.
3. `ROADMAP-TO-GOLD-MASTER.md` — release roadmap and milestone framing.
4. `GOLD-MASTER-CHECKLIST.md` — final Production/Enterprise Gold Master exit gates.
5. `prompts/phases/` — phase-level implementation prompts.
6. `prompts/specialists/` — specialist implementation prompts.
7. Existing architecture, deployment, security, eval, installer and workflow files remain supporting technical constraints and evidence sources.

## Target architecture

`Enterprise GUI → API Gateway → Identity/OIDC → Tenant Context → RBAC/ABAC + Policy/Confirmation → Intent Router → Planner/Orchestrator → Durable Task Store → Queue/Workers → Provider & Integration Fabric → Specialist Engines → Artifact Runtime → Audit/Event Stream → Observability → Release Gates`

## Execution method

For each bounded implementation slice:

`DISCOVER → DESIGN → IMPLEMENT → TEST → HARDEN → VERIFY → DOCUMENT → RELEASE EVIDENCE`

Always inspect `exec-planning.md`, select the highest-priority incomplete item with satisfied dependencies, execute only that bounded slice, and mark it complete only when implementation, tests, security/reliability review, documentation/runbooks, migration/rollback notes where applicable, and release evidence are complete.

## Enterprise Gold Master milestones

- **v5–v12:** Platform Core
- **v13–v25:** Universal Capability Runtime
- **v26–v40:** Reliability, Security & Governance
- **v41–v55:** Platform Engineering & Distribution
- **v56–v66:** Enterprise GA & Gold Master

## Production-ready definition

Do not call zanything production-ready merely because code builds. Production readiness requires proven clean installation, production identity/tenant/RBAC, durable DB/queue, externally managed secrets, integration safety controls, green test/security gates, operational observability/SLOs, backup/restore, upgrade/rollback, capacity/failure testing, DR evidence, completed runbooks/docs, and archived Gold Master release evidence.

## Pull request / release policy

- PRs must be current with `main` before merge.
- Required CI and security checks must pass; missing check execution is not equivalent to success.
- Resolve review threads and merge conflicts before merge.
- Dependency major-version PRs require compatibility review and green CI.
- Documentation, examples, release notes, GitHub templates and project ledgers must be updated when a change affects them.
- Prefer squash merge for bounded implementation slices unless repository policy requires another method.
