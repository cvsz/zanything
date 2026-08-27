# zanything

Enterprise Universal AI Operator — routes user intent across 20+ specialist modes (research, coding, security, data, documents, images, and more), plans execution workflows, and delivers verified outcomes.

## Current Status

> **v0.1.0 — Foundation.** Keyword-based routing is implemented. No production execution, persistence, authentication, or queue system exists yet. See [`roadmap/exec-planning.md`](roadmap/exec-planning.md) for the v5–v66 implementation ledger.

## Quick Start

```bash
# Clone and install
git clone https://github.com/cvsz/zanything.git && cd zanything
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Validate
pytest tests/ -v
ruff check src/ tests/
mypy src/

# Run locally
uvicorn zanything.app:app --reload --port 8080

# Docker
docker build -f deploy/docker/Dockerfile -t zanything:local .
docker run -p 8080:8080 zanything:local
```

## Repository Layout

```
src/zanything/      Python package (FastAPI application)
tests/              Pytest test suite
deploy/             Docker, Kubernetes, Helm, systemd, installer scripts
docs/               Architecture, development, deployment documentation
prompts/            System prompts, specialist definitions, phase directives
roadmap/            Execution planning, milestones, checklists
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/healthz` | Liveness probe |
| `GET` | `/readyz` | Readiness probe (no dependency checks yet) |
| `GET` | `/version` | Service name and version |
| `GET` | `/v1/capabilities` | Available routing modes and features |
| `POST` | `/v1/execute` | Route objective → modes → workflow plan |

## Roadmap

See [`roadmap/exec-planning.md`](roadmap/exec-planning.md) for the canonical v5–v66 implementation ledger.

**Next milestone:** v5 — Identity & Access Productionization (OIDC/JWT).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All PRs require CI green (tests, lint, type check, Docker build).

## License

See [LICENSE](LICENSE).
