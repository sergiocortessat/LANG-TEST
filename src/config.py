"""Load project settings from `.env`.

Stage 0 only needs Ollama's URL and model name. LangSmith keys stay
empty until we add tracing later.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# src/config.py → repo root (the folder that contains pyproject.toml)
ROOT = Path(__file__).resolve().parent.parent

# load_dotenv reads KEY=value lines into os.environ.
# Does not override variables already set in the shell.
load_dotenv(ROOT / ".env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
