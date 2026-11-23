from datetime import date

from src.rules import is_overdue


def test_past_due_date_is_overdue() -> None:
    assert is_overdue(date(2024, 6, 1), today=date(2026, 11, 23)) is True


def test_future_due_date_is_not_overdue() -> None:
    assert is_overdue(date(2027, 1, 1), today=date(2026, 11, 23)) is False
