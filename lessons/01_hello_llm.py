"""Stage 1 — first LangChain call to Ollama.

Run from the repo root:

    make lesson-1
    # or: uv run python lessons/01_hello_llm.py
"""

from langchain.messages import HumanMessage, SystemMessage

from src.llm import get_chat_model
from src.config import OLLAMA_BASE_URL, OLLAMA_MODEL


def main() -> None:
    print("Stage 1 — LangChain talks to Ollama")
    print(f"  url   : {OLLAMA_BASE_URL}")
    print(f"  model : {OLLAMA_MODEL}")
    print()

    # LangChain client (not the model itself, not Ollama the server).
    model = get_chat_model()

    # A chat model expects a list of messages, not a raw string.
    # SystemMessage = instructions. HumanMessage = the user turn.
    messages = [
        SystemMessage("You are a concise assistant. Reply in one short sentence."),
        HumanMessage("In one sentence, what is an invoice?"),
    ]

    # invoke() sends the messages to Ollama and waits for one reply.
    response = model.invoke(messages)

    print(f"response type : {type(response).__name__}")
    print(f"response       : {response}")
    print(f"content       : {response.content}")


if __name__ == "__main__":
    main()
