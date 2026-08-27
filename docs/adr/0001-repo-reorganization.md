# ADR-0001: Repository Reorganization

## Status

Accepted

## Date

2026-08-27

## Context

The zanything repository was in a flat structure with 85+ files at root level, including:
- 20 specialist prompt `.md` files (duplicated in `prompts/specialists/`)
- Deployment files mixed with application code
- 3 duplicate READMEs (`README.md`, `README (1).md`, `README (2).md`)
- Broken imports (`test_api.py` importing `enterprise.api.app` which didn't exist)
- Broken file paths (`app.py` GUI_DIR resolving 2 levels up)
- CI that only checked file existence, not application functionality
- Makefile with all-stub targets

## Decision

Reorganize into a standard Python package layout:
- `src/zanything/` — installable Python package
- `tests/` — pytest test suite
- `deploy/` — Docker, Kubernetes, Helm, systemd, scripts
- `docs/` — documentation
- `prompts/` — AI system prompts
- `roadmap/` — implementation planning

Use `pyproject.toml` with setuptools for package management.
Rewrite CI to actually install, test, lint, type-check, and Docker-build.
Fix all broken imports and file paths.
Remove fake readiness/capability claims.

## Consequences

- Fresh clones can install and run tests immediately
- CI fails when the application is broken, not just when docs are missing
- All deployment files have correct paths
- No misleading "integration-ready" or "enterprise-gui" feature claims
- Historical specialist `.md` files removed from root (consolidated versions in `prompts/specialists/`)
- Git history preserved via `git mv` for moved files
