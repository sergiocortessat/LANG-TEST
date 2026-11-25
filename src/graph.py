"""Stage 4 — LangGraph: order of steps, plus one if.

LangChain already knows how to talk to the model.
LangGraph only answers: what runs next?

A node is a Python function. It reads state and returns the keys it changed.
A tool is still a tool. Here the *node* calls lookup_supplier — we decide,
because the graph already knows the invoice is overdue.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph

from src.llm import get_chat_model
from src.parse_invoice import parse_invoice
from src.rules import is_overdue
from src.schemas import Invoice
from src.tools import lookup_supplier


class InvoiceState(TypedDict, total=False):
    invoice_text: str
    invoice: Invoice
    overdue: bool
    supplier_notes: str
    recommendation: str


def parse_node(state: InvoiceState) -> dict[str, Invoice]:
    """Step 1: same parse_invoice as Stage 2."""
    return {"invoice": parse_invoice(state["invoice_text"])}
    # return {"invoice": parse_invoice(state.get("invoice_text", ""))}


def overdue_node(state: InvoiceState) -> dict[str, bool]:
    """Step 2: same is_overdue as Stage 3. No LLM."""
    invoice = state["invoice"]
    return {"overdue": is_overdue(invoice.due_date)}


def route_after_overdue(
    state: InvoiceState,
) -> Literal["recommend_followup", "summarize_ok"]:
    """Conditional edge: pick the next *node name* from state."""
    if state["overdue"]:
        return "recommend_followup"
    return "summarize_ok"


def recommend_followup(state: InvoiceState) -> dict[str, str]:
    """Overdue path: we call the tool, then ask the LLM for one suggestion."""
    invoice = state["invoice"]
    notes = lookup_supplier.invoke({"name": invoice.supplier})
    response = get_chat_model().invoke(
        [
            SystemMessage(
                "You are an accounts-payable assistant. "
                "One or two short sentences. Do not send email or pay anyone."
            ),
            HumanMessage(
                f"Invoice {invoice.invoice_number} from {invoice.supplier} "
                f"({invoice.amount} {invoice.currency}) was due {invoice.due_date}. "
                f"Supplier registry: {notes}. Suggest a follow-up."
            ),
        ]
    )
    content = response.content
    text = content if isinstance(content, str) else str(content)
    return {"supplier_notes": notes, "recommendation": text}


def summarize_ok(state: InvoiceState) -> dict[str, str]:
    """On-time path: a short confirmation. No supplier lookup."""
    invoice = state["invoice"]
    response = get_chat_model().invoke(
        [
            SystemMessage("You are an accounts-payable assistant. One short sentence."),
            HumanMessage(
                f"Invoice {invoice.invoice_number} from {invoice.supplier} "
                f"is not overdue. Due {invoice.due_date}. Confirm it looks on time."
            ),
        ]
    )
    content = response.content
    text = content if isinstance(content, str) else str(content)
    return {"recommendation": text}


def build_invoice_graph():
    builder = StateGraph(InvoiceState)
    builder.add_node("parse", parse_node)
    builder.add_node("check_overdue", overdue_node)
    builder.add_node("recommend_followup", recommend_followup)
    builder.add_node("summarize_ok", summarize_ok)

    builder.add_edge(START, "parse")
    builder.add_edge("parse", "check_overdue")
    builder.add_conditional_edges(
        "check_overdue",
        route_after_overdue,
        {
            "recommend_followup": "recommend_followup",
            "summarize_ok": "summarize_ok",
        },
    )
    builder.add_edge("recommend_followup", END)
    builder.add_edge("summarize_ok", END)
    return builder.compile()
