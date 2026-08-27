# Development

## Prerequisites

- Python 3.11+ (tested on 3.11, 3.12, 3.13)
- Docker (for container builds)

## Local Setup

```bash
git clone https://github.com/cvsz/zanything.git
cd zanything
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Development Commands

```bash
# Run tests
pytest tests/ -v --tb=short

# Lint
ruff check src/ tests/

# Auto-format
ruff format src/ tests/

# Type check
mypy src/

# Run locally
uvicorn zanything.app:app --reload --port 8080

# Docker build
docker build -f deploy/docker/Dockerfile -t zanything:local .

# Full CI locally
make ci
```

Or use the Makefile:

```bash
make setup    # Create venv and install
make test     # Run pytest
make lint     # Run ruff check
make format   # Auto-format with ruff
make typecheck  # Run mypy
make build    # Docker build
make ci       # lint + typecheck + test + build
```

## Quality Expectations

- Keep changes small and reviewable.
- Add tests for behavior changes.
- Prefer deterministic and reproducible tooling.
- Do not commit secrets or local credentials.
- Do not weaken security or CI gates to obtain a passing build.
- All PRs must pass: pytest, ruff check, ruff format --check, mypy, Docker build.

## Project Structure

```
src/zanything/          Application package
  app.py                FastAPI application and endpoint definitions
  models.py             Pydantic request/response models
  routing.py            Intent routing logic (keyword-based)
  adapters/base.py      Integration adapter ABC (no implementations yet)
  gui/index.html        Admin console GUI
tests/                  Test suite
  conftest.py           Shared fixtures (TestClient)
  test_api.py           API endpoint tests
deploy/                 Deployment configurations
docs/                   Documentation
prompts/                AI system prompts and specialist definitions
roadmap/                Implementation planning and checklists
```

## Documentation

Update architecture, development, release, and ADR documentation when behavior or operational assumptions change.
