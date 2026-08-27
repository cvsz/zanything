SHELL := /bin/sh
.PHONY: help setup format lint typecheck test build security ci clean

help:
	@printf '%s\n' 'Targets: setup format lint typecheck test build security ci clean'

setup:
	python3 -m venv .venv
	.venv/bin/pip install -e ".[dev]"

format:
	ruff format src/ tests/

lint:
	ruff check src/ tests/

typecheck:
	mypy src/

test:
	pytest tests/ -v --tb=short

build:
	docker build -f deploy/docker/Dockerfile -t zanything:local .

security:
	ruff check src/ tests/ --select S

ci: lint typecheck test build

clean:
	rm -rf .venv dist *.egg-info .mypy_cache .pytest_cache .ruff_cache __pycache__
