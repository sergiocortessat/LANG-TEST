"""Stage 2 — prompt templates and structured output.

Run from the repo root:

    make lesson-2
"""

from src.parse_invoice import INVOICE_PROMPT, parse_invoice
from src.schemas import SAMPLE_INVOICE_TEXT


def main() -> None:
    print("Stage 2 — prompts + structured output")
    print()
    print("Input text:")
    print(SAMPLE_INVOICE_TEXT)

    # The template is reusable. {invoice_text} is filled at invoke time.
    messages = INVOICE_PROMPT.invoke({"invoice_text": SAMPLE_INVOICE_TEXT})
    print("Messages after filling the template:")
    for message in messages.to_messages():
        print(f"  [{message.type}] {message.content[:80]!r}...")
    print()

    invoice = parse_invoice(SAMPLE_INVOICE_TEXT)
    print(f"result type : {type(invoice).__name__}")
    print(f"supplier    : {invoice.supplier}")
    print(f"number      : {invoice.invoice_number}")
    print(f"amount      : {invoice.amount} {invoice.currency}")
    print(f"due_date    : {invoice.due_date}  (Python type: {type(invoice.due_date).__name__})")
    print(f"description : {invoice.description}")


if __name__ == "__main__":
    main()
