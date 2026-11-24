"""Boundary checks for raw transaction data (CSV rows, CLI input).

models.py already validates invariants inside Transaction.__init__ (amount
must be positive, category must be known...). This module sits one step
before that: it takes raw, possibly dirty data -- strings from a CSV row,
arguments typed at the CLI -- and turns it into something clean enough for
Transaction.from_dict to accept, raising ValueError with a message a human
can act on if it can't.
"""

from .models import Transaction

REQUIRED_FIELDS = ["id", "date", "kind", "category", "amount"]


def clean_row(row, row_number=None):
    """Normalize a raw dict into the shape Transaction.from_dict expects.

    Strips whitespace, lowercases kind/category, uppercases currency, and
    converts amount to float. Raises ValueError naming the missing or
    malformed field if it can't.
    """
    location = f"Row {row_number}" if row_number is not None else "Input"

    for field in REQUIRED_FIELDS:
        if field not in row or str(row[field]).strip() == "":
            raise ValueError(f"{location}: missing required field '{field}'.")

    cleaned = {
        "id": str(row["id"]).strip(),
        "date": str(row["date"]).strip(),
        "kind": str(row["kind"]).strip().lower(),
        "category": str(row["category"]).strip().lower(),
        "currency": str(row.get("currency") or "EUR").strip().upper(),
    }

    try:
        cleaned["amount"] = float(row["amount"])
    except (TypeError, ValueError):
        raise ValueError(f"{location}: amount must be a number, got {row['amount']}.")

    return cleaned


def build_transaction(row, row_number=None):
    """Clean a raw row and construct a Transaction from it.

    Any ValueError raised by the Transaction constructor (unknown kind,
    unknown category, non-positive amount) is caught here and re-raised
    with the row location added, so callers always get a message that
    points to the exact row.
    """
    location = f"Row {row_number}" if row_number is not None else "Input"
    cleaned = clean_row(row, row_number)
    try:
        return Transaction.from_dict(cleaned)
    except ValueError as exc:
        raise ValueError(f"{location}: {exc}")
