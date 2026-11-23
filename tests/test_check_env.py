from check_env import model_is_available


def test_exact_name_matches() -> None:
    assert model_is_available("llama3.2:latest", ["llama3.2:latest"])


def test_untagged_name_matches_latest() -> None:
    assert model_is_available("llama3.2", ["llama3.2:latest"])


def test_missing_model_does_not_match() -> None:
    assert not model_is_available("llama3.2", ["qwen2.5-coder:7b"])
