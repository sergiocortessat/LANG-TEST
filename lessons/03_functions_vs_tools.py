"""Stage 3 — a Python function vs a LangChain tool.

Run from the repo root:

    make lesson-3
"""

from datetime import date

from langchain.messages import HumanMessage, SystemMessage, ToolMessage

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
        due_date=date(2024, 6, 1),
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

    print("PART B — first invoke. The model may *request* a tool (content often empty).")
    model = get_chat_model().bind_tools([lookup_supplier])
    messages: list = [
        SystemMessage(
            "You look up suppliers. If you need registry data, "
            "call lookup_supplier. Do not invent payment terms."
        ),
        HumanMessage(f"What are the payment terms for {invoice.supplier}?"),
    ]
    first = model.invoke(messages)

    print(f"  response type : {type(first).__name__}")
    print(f"  content       : {first.content!r}")
    print(f"  tool_calls    : {first.tool_calls}")
    print()

    if not first.tool_calls:
        print("  The model answered in text and did not request the tool.")
        print("  That can happen with local models. The important idea:")
        print("  a tool_call is a *request*, not the function already running.")
        return

    print("PART C — we run the tool ourselves (the model cannot).")
    messages.append(first)
    for tool_call in first.tool_calls:
        print(f"  requested: {tool_call['name']}({tool_call['args']})")
        result = lookup_supplier.invoke(tool_call["args"])
        print(f"  result   : {result}")
        # ToolMessage = "here is what that function returned"
        messages.append(
            ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )
        )
    print()

    print('--------------------------------');
    print(messages);
    print('--------------------------------');

    print("PART D — second invoke. Now the model can write a sentence using the result.")
    final = model.invoke(messages)
    print(f"  content : {final.content}")
    print(f"  tool_calls this time : {final.tool_calls}")


if __name__ == "__main__":
    main()
