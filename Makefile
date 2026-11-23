# Shortcuts like "npm run …" — run from repo root

UV := $(or $(shell command -v uv 2>/dev/null),$(HOME)/.local/bin/uv)

.PHONY: install help sync check-env test mypy

help:
	@echo "make sync         — uv sync (create/update .venv from pyproject.toml)"
	@echo "make install      — alias for make sync"
	@echo "make check-env    — Stage 0: verify project Python can reach Ollama"
	@echo "make test         — run pytest"
	@echo "make mypy         — run mypy"
	@echo ""
	@echo "Optional: source .venv/bin/activate  (uv run works without activating)"

sync install:
	$(UV) sync --all-groups

check-env:
	$(UV) run python -m src.main

test:
	$(UV) run pytest

mypy:
	$(UV) run mypy
