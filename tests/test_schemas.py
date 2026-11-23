from datetime import date

from src.schemas import Invoice


def test_invoice_accepts_iso_due_date_string() -> None:
    invoice = Invoice(
        supplier="Flower Export Ltd.",
        invoice_number="INV-1024",
        amount=2500,
        currency="EUR",
        due_date="2024-06-01",
        description="Flower shipment",
    )
    assert invoice.due_date == date(2024, 6, 1)
    assert invoice.amount == 2500.0
