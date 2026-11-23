# Shortcuts like "npm run dev" — run from repo root

UV := $(or $(shell command -v uv 2>/dev/null),$(HOME)/.local/bin/uv)

# Uvicorn import paths (module:variable).
APP_MAIN := src.main:app

UVICORN_HOST := 127.0.0.1
UVICORN_PORT := 8000
UVICORN_PLAYGROUND_PORT := 8001


.PHONY: install help sync test mypy

help:
	@echo "make sync         — uv sync (create/update .venv from pyproject.toml)"
	@echo "make install      — alias for make sync"
	@echo "make dev          — primary API (uvicorn, port $(UVICORN_PORT))"
	@echo "make test         — run pytest"
	@echo "make mypy         — run mypy"
	@echo ""
	@echo "Optional: source .venv/bin/activate  (uv run works without activating)"

sync install:
	$(UV) sync --all-groups

dev:
	$(UV) run uvicorn $(APP_MAIN) --reload --host $(UVICORN_HOST) --port $(UVICORN_PORT)

test:
	$(UV) run pytest

mypy:
	$(UV) run mypy