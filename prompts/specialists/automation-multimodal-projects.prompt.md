# Automation / Multimodal / Project Execution Implementation Prompt

Implement production Automation, Multimodal and Project Execution capabilities for zanything.

## Automation
- Durable workflow definitions.
- Trigger/schedule/manual execution abstraction.
- Idempotent side effects.
- Timeouts, retries, backoff and DLQ.
- Approval gates for high-impact actions.
- Audit trail and replay-safe execution.
- Secret references rather than embedded credentials.

## Multimodal
- Unified model for text, files, images, tabular data, code and generated artifacts.
- Source provenance and attachment lifecycle.
- Tenant-safe storage and authorization.
- Mixed-input execution graph.
- Clear unsupported-input and partial-failure behavior.

## Project Execution
Use:
`DISCOVER → DESIGN → IMPLEMENT → TEST → HARDEN → VERIFY → DOCUMENT → RELEASE EVIDENCE`

- Persistent project state.
- Milestones/workstreams/dependencies.
- Highest-priority unblocked bounded slice selection.
- Blockers and approval state.
- Resumable execution.
- Completion ledger.
- Acceptance and release gates.

## Tests
- duplicate/replayed automation events
- retry/idempotency behavior
- cancellation and resume
- approval enforcement
- attachment authorization
- cross-tenant leakage prevention
- partial multimodal failure
- project state recovery

Completion requires durable implementation, tests, auditability, docs/runbooks and release evidence.
