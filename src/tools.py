"""LangChain tools: functions the *model* is allowed to request.

A tool is still a Python function. The extra is metadata (name, docstring,
arguments) that LangChain shows to llama3.2. The model does not run the
code itself — it only asks. Our program runs it afterwards.
"""

from __future__ import annotations

from langchain.tools import tool

# Fake company database. In a real app this would be an HTTP API or SQL.
SUPPLIERS: dict[str, dict[str, str]] = {
    "Flower Export Ltd.": {
        "status": "trusted",
        "payment_terms": "Net 30",
        "notes": "Perishable goods. Contact: ap@flowerexport.example",
    },
    "Acme Supplies": {
        "status": "new",
        "payment_terms": "Net 14",
        "notes": "First invoice. Ask finance to confirm the IBAN.",
    },
}


@tool
def lookup_supplier(name: str) -> str:
    """Look up a supplier in the internal company registry.

    Use this when you need payment terms or trust status for a supplier
    name from an invoice. Pass the company name exactly if possible.
    """
    record = SUPPLIERS.get(name)
    if record is None:
        return f"No registry entry for {name!r}."
    return (
        f"status={record['status']}; "
        f"payment_terms={record['payment_terms']}; "
        f"notes={record['notes']}"
    )
