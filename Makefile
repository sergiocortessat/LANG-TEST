# Shortcuts like "npm run …" — run from repo root

UV := $(or $(shell command -v uv 2>/dev/null),$(HOME)/.local/bin/uv)

.PHONY: install help sync check-env lesson-1 lesson-2 lesson-3 lesson-4 test mypy

help:
	@echo "make sync         — uv sync (create/update .venv from pyproject.toml)"
	@echo "make install      — alias for make sync"
	@echo "make check-env    — Stage 0: verify project Python can reach Ollama"
	@echo "make lesson-1     — Stage 1: first LangChain call to Ollama"
	@echo "make lesson-2     — Stage 2: prompt template + structured Invoice"
	@echo "make lesson-3     — Stage 3: Python function vs LangChain tool"
	@echo "make lesson-4     — Stage 4: LangGraph overdue branch"
	@echo "make test         — run pytest"
	@echo "make mypy         — run mypy"
	@echo ""
	@echo "Optional: source .venv/bin/activate  (uv run works without activating)"

sync install:
	$(UV) sync --all-groups

check-env:
	$(UV) run python -m src.main

lesson-1:
	$(UV) run python lessons/01_hello_llm.py

lesson-2:
	$(UV) run python lessons/02_prompts_structured.py

lesson-3:
	$(UV) run python lessons/03_functions_vs_tools.py

lesson-4:
	$(UV) run python lessons/04_langgraph.py

test:
	$(UV) run pytest

mypy:
	$(UV) run mypy
