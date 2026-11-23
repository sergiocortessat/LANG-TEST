"""Stage 0: prove project Python can reach Ollama.

This does not call LangChain. It uses the standard library to hit
Ollama's HTTP API, the same API LangChain will use in Stage 1.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL, ROOT


def model_is_available(requested: str, installed: list[str]) -> bool:
    """Return True if `requested` is in `ollama list`.

    Ollama tags a default as `name:latest`, so `llama3.2` matches
    `llama3.2:latest`.
    """
    for name in installed:
        if name == requested or name.startswith(f"{requested}:"):
            return True
    return False


def fetch_ollama_models(base_url: str) -> list[str]:
    url = f"{base_url}/api/tags"
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=5) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [item["name"] for item in payload.get("models", [])]


def main() -> int:
    print("Stage 0 — environment check")
    print(f"  project root : {ROOT}")
    print(f"  python       : {sys.executable}")
    print(f"  python ver   : {sys.version.split()[0]}")
    print(f"  ollama url   : {OLLAMA_BASE_URL}")
    print(f"  ollama model : {OLLAMA_MODEL}")
    print()

    try:
        installed = fetch_ollama_models(OLLAMA_BASE_URL)
    except urllib.error.URLError as exc:
        print("Ollama is not reachable.")
        print("Start it with:  ollama serve")
        print(f"Details: {exc}")
        return 1

    print("Installed Ollama models:")
    for name in installed:
        marker = "  <-- selected" if model_is_available(OLLAMA_MODEL, [name]) else ""
        print(f"  - {name}{marker}")
    print()

    if not model_is_available(OLLAMA_MODEL, installed):
        print(f"Model {OLLAMA_MODEL!r} is not installed.")
        print(f"Pull it with:  ollama pull {OLLAMA_MODEL}")
        return 1

    print("OK — project Python can see Ollama and the selected model.")
    print("Stop here. Stage 1 will send the first LangChain prompt.")
    return 0
