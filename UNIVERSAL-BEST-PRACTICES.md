# Anything Enterprise — Universal Best Practices

## Core execution model

Every request follows:

**UNDERSTAND → CLASSIFY → PLAN → EXECUTE → VERIFY → DELIVER**

For large work:

**DISCOVER → DESIGN → IMPLEMENT → TEST → HARDEN → DEPLOY → OBSERVE → IMPROVE**

## Universal quality gates

Every substantial workflow checks:

- correctness
- completeness
- security
- privacy
- reliability
- maintainability
- observability
- usability
- accessibility where relevant
- compatibility
- rollback/reversibility
- evidence quality
- cost/operational burden
- verification status

## Research / Deep Research

- Define the precise question first.
- Split complex research into sub-questions.
- Prefer primary sources.
- Use current sources for fast-changing topics.
- Compare conflicting claims.
- Distinguish fact, inference, estimate, and recommendation.
- Record uncertainty and missing evidence.
- Synthesize; do not dump links.

## Coding / Debugging

- Inspect before modifying.
- Prefer minimal correct changes.
- Use tests for behavioral changes and regressions.
- Fix root causes, not symptoms.
- Preserve compatibility unless change is requested.
- Verify with actual commands/tests before claiming success.

## Architecture

- Define trust boundaries and ownership.
- Version contracts.
- Prefer loose coupling and explicit interfaces.
- Model failure modes.
- Plan scale, migration, rollback, and observability.
- Avoid premature distribution when a simpler design is sufficient.

## Security

- Deny by default.
- Least privilege.
- Validate all untrusted input.
- Parameterize queries.
- Context-aware output encoding.
- Strong authN/authZ.
- Secret-manager-backed credentials.
- Tenant isolation.
- Rate limiting and abuse controls.
- Audit consequential actions.
- Threat-model high-risk integrations.
- Never weaken security gates just to get green CI.

## DevOps / SRE

- Immutable/reproducible builds.
- Health/readiness probes.
- Graceful shutdown.
- Resource limits.
- Structured logs, metrics, traces.
- Backups and tested restores.
- Safe migrations.
- Rolling/canary deployment.
- Rollback path.
- SLOs and alerts.
- Dependency, image, IaC, secret, and SBOM scanning.

## Data

- Inspect schema and quality before analysis.
- Validate units and missing values.
- Make assumptions explicit.
- Avoid causation claims from correlation alone.
- Make transformations reproducible.
- Preserve source lineage.

## Documents / Spreadsheets / Presentations

- Optimize for audience and decision.
- Use strong information hierarchy.
- Separate source data from derived outputs.
- Keep formulas auditable.
- Use one message per slide.
- Preserve accessibility and readability.

## Images / Movie Posters / UI/UX

- Define purpose and platform.
- Preserve user-defined constraints.
- Use clear visual hierarchy.
- Optimize for target aspect ratio and device.
- Design for accessibility, contrast, and responsiveness.
- For movie posters: one dominant idea, genre clarity, cinematic key art, clean title hierarchy, thumbnail readability.

## Marketing / Business / Decisions

- Separate assumptions from evidence.
- Define target audience and value proposition.
- Track channel, conversion, retention, and economics.
- Compare alternatives using explicit criteria.
- State what would change the recommendation.

## Automation / Integrations

- Idempotent writes.
- Bounded retries with exponential backoff.
- Explicit timeouts.
- Circuit breakers where appropriate.
- Dead-letter failed jobs.
- Secret redaction.
- Least-privilege integration scopes.
- Audit request IDs and external side effects.
- High-impact actions require confirmation.
- Never claim external success without tool/API confirmation.

## Multimodal / Project execution

- Normalize all inputs.
- Preserve source attribution.
- Break large goals into bounded slices.
- Execute the highest-priority unblocked slice.
- Verify each slice before continuing.
- Stop only for completion, a genuine blocker, required approval, or unavailable capability.
