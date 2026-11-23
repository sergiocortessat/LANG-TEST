from src.llm import ollama_model_id


def test_ollama_model_id_uses_provider_prefix() -> None:
    assert ollama_model_id("llama3.2") == "ollama:llama3.2"
