"""Stage 3 — a Python function vs a LangChain tool.

Run from the repo root:

    make lesson-3
"""

from langchain.messages import HumanMessage, SystemMessage

from src.llm import get_chat_model
from src.rules import is_overdue
from src.schemas import Invoice
from src.tools import lookup_supplier


def main() -> None:
    # Stage 2 already taught parsing. Here we build the same Invoice
    # without calling the LLM again, so this lesson stays focused.
    invoice = Invoice(
        supplier="Flower Export Ltd.",
        invoice_number="INV-1024",
        amount=2500,
        currency="EUR",
        due_date="2024-06-01",
        description="Flower shipment",
    )

    print("Stage 3 — functions vs tools")
    print(f"Invoice: {invoice.invoice_number} / {invoice.supplier}")
    print()

    print("PART A — plain Python. We decide to call it.")
    overdue = is_overdue(invoice.due_date)
    print(f"  is_overdue({invoice.due_date}) -> {overdue}")
    print("  No Ollama. No LangChain. Just dates.")
    print()

    print("PART B — a tool. The model may *request* it.")
    model = get_chat_model().bind_tools([lookup_supplier])
    response = model.invoke(
        [
            SystemMessage(
                "You look up suppliers. If you need registry data, "
                "call lookup_supplier. Do not invent payment terms."
            ),
            HumanMessage(
                f"What are the payment terms for {invoice.supplier}?"
            ),
        ]
    )

    print(f"  response type : {type(response).__name__}")
    print(f"  content       : {response.content!r}")
    print(f"  tool_calls    : {response.tool_calls}")
    print()

    if not response.tool_calls:
        print("  The model answered in text and did not request the tool.")
        print("  That can happen with local models. The important idea:")
        print("  a tool_call is a *request*, not the function already running.")
        return

    print("PART C — we run the tool ourselves (the model cannot).")
    for tool_call in response.tool_calls:
        print(f"  requested: {tool_call['name']}({tool_call['args']})")
        result = lookup_supplier.invoke(tool_call["args"])
        print(f"  result   : {result}")

    print()
    print("Reminder: is_overdue was our call. lookup_supplier was the model's ask.")


if __name__ == "__main__":
    main()
