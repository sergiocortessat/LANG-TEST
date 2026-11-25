from datetime import date

from src.graph import route_after_overdue
from src.schemas import Invoice


def _invoice() -> Invoice:
    return Invoice(
        supplier="Flower Export Ltd.",
        invoice_number="INV-1024",
        amount=2500,
        currency="EUR",
        due_date=date(2024, 6, 1),
        description="Flower shipment",
    )


def test_overdue_routes_to_followup() -> None:
    assert (
        route_after_overdue({"invoice": _invoice(), "overdue": True})
        == "recommend_followup"
    )


def test_on_time_routes_to_summarize() -> None:
    assert (
        route_after_overdue({"invoice": _invoice(), "overdue": False})
        == "summarize_ok"
    )
