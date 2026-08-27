# About zanything

`zanything` is the implementation repository for **Anything Enterprise Universal Operator**: a universal AI operator platform intended to unify research, engineering, security, operations, data, office artifacts, visual creation, product design, business workflows, automation, multimodal work and end-to-end project execution behind shared enterprise controls.

## Scope

The target capability set includes:

- Research and Deep Research
- Coding and Debugging
- Architecture and Security
- DevOps / SRE
- Data analysis and data workflows
- Documents, Spreadsheets and Presentations
- Images and Movie Posters
- UI/UX and design-system workflows
- Marketing and Business strategy
- Automation and external integrations
- Decision Making
- Multimodal execution
- End-to-end Project Execution

## Enterprise target architecture

`Enterprise GUI → API Gateway → Identity/OIDC → Tenant Context → RBAC/ABAC + Policy/Confirmation → Intent Router → Planner/Orchestrator → Durable Task Store → Queue/Workers → Provider & Integration Fabric → Specialist Engines → Artifact Runtime → Audit/Event Stream → Observability → Release Gates`

## Engineering principles

zanything should be:

- secure by default
- deny-by-default at authorization boundaries
- tenant-aware and tenant-isolated
- automation-first
- observable and auditable
- durable and recoverable
- testable and evidence-driven
- upgradeable and rollback-safe
- modular, extensible and provider-neutral where practical
- accessible and responsive at the GUI layer
- explicit about uncertainty, failed verification and incomplete production readiness

Security and quality checks should be fixed rather than bypassed. CI, migrations, backups, release evidence, documentation, observability, operational runbooks and recovery are part of the product rather than afterthoughts.

## Implementation system

Canonical project execution is defined by:

- `prompts/MASTER-IMPLEMENTATION.prompt.md`
- `exec-planning.md`
- `ROADMAP-TO-GOLD-MASTER.md`
- `GOLD-MASTER-CHECKLIST.md`
- `prompts/phases/`
- `prompts/specialists/`

The execution loop is:

`DISCOVER → DESIGN → IMPLEMENT → TEST → HARDEN → VERIFY → DOCUMENT → RELEASE EVIDENCE`

## Milestones

- v5–v12 — Platform Core
- v13–v25 — Universal Capability Runtime
- v26–v40 — Reliability, Security & Governance
- v41–v55 — Platform Engineering & Distribution
- v56–v66 — Enterprise GA & Gold Master

## Production readiness

The repository must not describe itself as production-ready solely because scaffolding exists or CI builds. Production readiness requires implementation and evidence for identity, authorization, tenant isolation, durable state/queue, secrets, security gates, observability/SLOs, backup/restore, upgrade/rollback, load/failure testing, DR, documentation/runbooks and the Gold Master exit criteria.

## Repository

- GitHub: `cvsz/zanything`
- Default branch: `main`
