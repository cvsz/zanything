# Changelog

All notable changes to zanything are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

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

