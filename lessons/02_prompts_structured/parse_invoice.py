"""Turn messy invoice text into an Invoice object.

Stage 2 pieces:
- ChatPromptTemplate: fill {invoice_text} without concatenating strings.
- with_structured_output: ask the model for Invoice, not an AIMessage paragraph.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from src.llm import get_chat_model
from src.schemas import Invoice

INVOICE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Extract invoice fields from the text. "
            "due_date must be YYYY-MM-DD. "
            "amount must be a number with no thousands separators. "
            "currency must be a 3-letter code such as EUR.",
        ),
        ("human", "{invoice_text}"),
    ]
)


def parse_invoice(invoice_text: str) -> Invoice:
    """Return a validated Invoice, or raise if the model/schema fail."""
    model = get_chat_model().with_structured_output(Invoice)
    messages = INVOICE_PROMPT.invoke({"invoice_text": invoice_text})
    result = model.invoke(messages)
    print(f"result: {result}")
    print("--------------------------------")
    if not isinstance(result, Invoice):
        raise TypeError(f"Expected Invoice, got {type(result).__name__}: {result!r}")
    return result
