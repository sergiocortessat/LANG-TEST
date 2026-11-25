"""Stage 4 — LangGraph: nodes, state, one conditional branch.

Run from the repo root:

    make lesson-4
"""

from src.graph import build_invoice_graph
from src.schemas import SAMPLE_INVOICE_TEXT


def main() -> None:
    graph = build_invoice_graph()

    print("Stage 4 — LangGraph")
    print()
    print("The graph (mermaid). Conditional edge is the overdue if:")
    print(graph.get_graph().draw_mermaid())
    print()

    print("Input text:")
    print(SAMPLE_INVOICE_TEXT)

    result = graph.invoke({"invoice_text": SAMPLE_INVOICE_TEXT})
    invoice = result["invoice"]

    print(f"parsed      : {invoice.invoice_number} / {invoice.supplier}")
    print(f"overdue     : {result['overdue']}")
    print(f"notes       : {result.get('supplier_notes', '(skipped — on-time path)')}")
    print(f"next action : {result['recommendation']}")


if __name__ == "__main__":
    main()
