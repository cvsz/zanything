# Changelog

All notable changes to zanything are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added - v9-v12 Platform Core Services
- Universal Integration Fabric adapter contracts (`GitHubAdapter`, `SlackAdapter`) with health probes & scopes (`src/zanything/adapters/__init__.py`)
- Secret Management provider abstraction, `EnvSecretProvider`, and `SecretRedactor` (`src/zanything/secrets/__init__.py`)
- Policy & Confirmation Engine with `ActionClass` risk categorization (`READ_ONLY`, `REVERSIBLE_WRITE`, `HIGH_IMPACT`) and `PolicyEngine` evaluator (`src/zanything/policy/__init__.py`)
- 4 integration tests covering integration execution, secret redaction, env secret resolution, and policy evaluation (`tests/test_platform.py`)

### Added - v8 Provider Runtime
- Standardized `ProviderRequest`, `ProviderResponse`, `ModelSpec`, and `ProviderType` contracts (`src/zanything/providers/__init__.py`)
- Stateful `CircuitBreaker` pattern protecting providers from cascading failures (`src/zanything/providers/circuit_breaker.py`)
- `ProviderRouter` with failover policy chains and per-tenant cost/token tracking (`src/zanything/providers/router.py`)
- 3 integration tests covering provider routing, failover, circuit breaker transitions, and cost aggregation (`tests/test_providers.py`)

### Added - v7 Queue & Worker Fabric
- Durable Queue backend interface & `AsyncMemoryQueue` with Priority scheduling (`CRITICAL`, `HIGH`, `NORMAL`, `LOW`) (`src/zanything/queue/backend.py`)
- Exponential retry policies and Dead Letter Queue (DLQ) isolation
- Async `Worker` pool with concurrency limits and `WorkerHeartbeat` saturation metrics (`src/zanything/queue/worker.py`)
- 4 integration tests verifying queue priority, worker execution, retries, DLQ, and heartbeats (`tests/test_queue.py`)

### Added - v6 Durable Data Runtime
- Async SQLAlchemy 2.0 database engine & session manager with connection pooling (`src/zanything/db/__init__.py`)
- Persistent models for Tasks, Idempotency Keys, and Audit Events with tenant index scoping (`src/zanything/db/models.py`)
- Tenant-isolated async repositories: `TaskRepository`, `IdempotencyRepository`, `AuditRepository` (`src/zanything/db/repositories.py`)
- 3 async integration tests verifying tenant isolation, idempotency persistence, and audit logging (`tests/test_db.py`)

### Added - v5 Identity & Access Productionization
- Real OIDC / JWT verification with JWKS and symmetric/asymmetric support (`src/zanything/auth/jwt.py`)
- Tenant-aware principal model (`src/zanything/auth/__init__.py`)
- RBAC and ABAC policy evaluation and role guard dependencies (`src/zanything/auth/dependencies.py`)
- Service account API Key authentication pathway (`X-API-Key`)
- Admin role management API `/v1/admin/roles` and identity inspector `/v1/me`
- Access-review and emergency break-glass runbook (`docs/runbooks/access-review-breakglass.md`)
- 9 AuthN/AuthZ/Tenant integration tests (`tests/test_auth.py`)

### Added - NEXT-002 Runtime Foundation
- Enterprise runtime configuration model with Pydantic `BaseSettings` (`src/zanything/config.py`)
- RFC 7807 Problem Details compliant error handling & exception contracts (`src/zanything/errors.py`)
- Structured JSON logging with `ContextVar` correlation ID & tenant tracking (`src/zanything/logging.py`)
- Request context middleware propagating `X-Request-ID` and timing latency
- Application factory pattern `create_app()` with async `lifespan` management

## [0.1.0] — 2026-08-27

### Added

- Python package structure (`src/zanything/`) with `pyproject.toml`
- Installable package with `pip install -e ".[dev]"`
- Proper test suite in `tests/` with 11 passing tests
- Real CI: Python 3.11/3.12/3.13 matrix, pytest, ruff lint, ruff format, mypy, Docker build
- CodeQL analysis for Python (alongside existing Actions analysis)
- ADR-0001 documenting repository reorganization decision

### Changed

- Reorganized repository: deployment → `deploy/`, docs → `docs/`, roadmap → `roadmap/`
- Moved application code to `src/zanything/` package
- Refactored `app.py` into `app.py`, `models.py`, `routing.py` modules
- `/readyz` returns honest `"no-dependencies"` status instead of fake `"ready"`
- `/v1/execute` returns `"routed"` / `"dry-run-planned"` instead of misleading `"accepted"` / `"planned"`
- `/v1/capabilities` removed false feature claims (`integration-ready`, `enterprise-gui`, `idempotency-header-ready`)
- Makefile targets are real commands instead of placeholder echo statements
- Version reset to `0.1.0` (no production release has occurred)

### Fixed

- Test import path: `from enterprise.api.app` → `from zanything.app`
- GUI directory resolution: was going 2 levels up from root, now correctly relative to app.py
- Dockerfile: references correct `src/zanything/` package layout
- docker-compose.yml: correct build context and Dockerfile path
- Issue template URL: `cvsz/ztemplate` → `cvsz/zanything`

### Removed

- 20 duplicate specialist `.md` files from root (consolidated in `prompts/specialists/`)
- Duplicate READMEs (`README (1).md`, `README (2).md`)
- Duplicate deployment file (`deployment (3).yaml`)
- Stale `SHA256SUMS.txt` (no release artifacts exist)
- Stale root `github-actions.yml` (real CI at `.github/workflows/ci.yml`)
- Stale root prompt docs (content in `prompts/` already)

### Security

- Fixed stale issue template security URL

