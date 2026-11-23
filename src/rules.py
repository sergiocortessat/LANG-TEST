"""Deterministic invoice rules. No LLM, no LangChain.

If the answer is a calendar comparison, a Python function is enough.
The model does not get a vote here.
"""

from __future__ import annotations

from datetime import date


def is_overdue(due_date: date, today: date | None = None) -> bool:
    """Return True if the due date is before today.

    `today` is injectable so tests do not depend on the real clock.
    """
    current = today or date.today()
    return due_date < current
