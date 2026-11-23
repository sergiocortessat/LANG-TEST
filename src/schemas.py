"""Pydantic shapes for the Invoice Assistant.

A schema is a contract: field names, types, and descriptions.
LangChain sends those descriptions to the model so it fills the
right JSON instead of writing a paragraph.
"""

from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

SAMPLE_INVOICE_TEXT = """\
Supplier: Flower Export Ltd.
Invoice number: INV-1024
Amount: 2500 EUR
Due date: 2024-06-01
Description: Flower shipment
"""


class Invoice(BaseModel):
    """Fields we need from an invoice. Keep this small on purpose."""

    supplier: str = Field(description="Company that issued the invoice")
    invoice_number: str = Field(description="Invoice id, for example INV-1024")
    amount: float = Field(description="Total as a number, no thousands separators")
    currency: str = Field(description="Three-letter currency code, for example EUR")
    due_date: date = Field(description="Payment due date in ISO format YYYY-MM-DD")
    description: str = Field(description="Short description of what was billed")
