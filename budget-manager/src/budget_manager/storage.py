"""Load/save transactions to a CSV file."""

import csv
from pathlib import Path

from .validation import build_transaction

FIELDNAMES = ["id", "date", "kind", "category", "amount", "currency"]


def load_transactions(path):
    """Read a CSV file and return (transactions, errors).

    Invalid or duplicate rows are skipped and reported in errors instead of
    crashing the whole load -- a partial load that doesn't report what it
    rejected would make totals unreliable.
    """
    path = Path(path)
    transactions = []
    errors = []
    seen_ids = set()

    if not path.exists():
        return transactions, errors

    with path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    for row_number, row in enumerate(rows, start=2):  # row 1 is the header
        try:
            transaction = build_transaction(row, row_number)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if transaction.id in seen_ids:
            errors.append(f"Row {row_number}: duplicate id '{transaction.id}', skipped.")
            continue

        seen_ids.add(transaction.id)
        transactions.append(transaction)

    return transactions, errors


def save_transactions(path, transactions):
    """Write all transactions to a CSV file, replacing its current contents."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow(transaction.to_dict())
