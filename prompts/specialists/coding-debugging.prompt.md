# Coding / Debugging Implementation Prompt

Implement production Coding and Debugging capabilities for zanything.

## Coding requirements
- Repository/workspace abstraction with branch/worktree isolation.
- Explicit task scope and acceptance criteria.
- Test-first changes where practical.
- Build, lint, typecheck, unit/integration/E2E orchestration.
- Minimal correct patches that preserve contracts by default.
- Dependency/update handling with compatibility review.
- Artifact output for patches, logs, test summaries, and release evidence.

## Debugging requirements
Use `OBSERVE → REPRODUCE → ISOLATE → HYPOTHESIZE → TEST → FIX ROOT CAUSE → REGRESSION TEST → VERIFY`.

- Capture reproducible failure evidence.
- Prefer one root-cause hypothesis at a time.
- Prevent broad speculative fixes.
- Add regression tests for resolved defects.
- Preserve security gates and fail-closed behavior.

## Security boundaries
Validate filesystem containment, path traversal, shell/process execution, secret handling, network egress, dependency/supply-chain changes, untrusted code, tenant isolation, and generated artifact permissions.

## Test requirements
- isolated workspace behavior
- dirty repository handling
- failed command propagation
- timeout/cancellation
- regression test enforcement
- security-scan integration
- CI evidence ingestion
- no false green status

## Definition of done
Implementation, regression evidence, docs, CI integration, security review, and remaining limitations must be explicit.
