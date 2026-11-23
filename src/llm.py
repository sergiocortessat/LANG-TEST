"""Build the LangChain chat model that talks to local Ollama.

Stage 1: one helper. No prompts templates, tools, or graphs yet.
"""

from __future__ import annotations

from langchain.chat_models import init_chat_model
from langchain_core.language_models.chat_models import BaseChatModel

from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def ollama_model_id(model_name: str) -> str:
    """LangChain provider prefix: 'ollama:llama3.2'."""
    return f"ollama:{model_name}"


def get_chat_model() -> BaseChatModel:
    """Return a chat model pointed at this project's Ollama settings.

    init_chat_model is LangChain's factory: the 'ollama:' prefix loads
    langchain-ollama. base_url is the same server Stage 0 pinged with HTTP.
    """
    return init_chat_model(
        ollama_model_id(OLLAMA_MODEL),
        temperature=0,
        base_url=OLLAMA_BASE_URL,
    )
