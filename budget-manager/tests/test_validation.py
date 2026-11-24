from budget_manager.validation import build_transaction


def test_build_transaction_cleans_dirty_input():
    """Normal case: whitespace/case-mangled input is cleaned before building the Transaction."""
    row = {
        "id": " T010 ",
        "date": "2026-02-01",
        "kind": "Income",
        "category": "Salary",
        "amount": "1200",
        "currency": "eur",
    }

    t = build_transaction(row, row_number=2)

    assert t.id == "T010"
    assert t.kind == "income"
    assert t.category == "salary"
    assert t.amount == 1200.0
    assert t.currency == "EUR"


def test_build_transaction_reports_missing_field_with_row_number():
    """Boundary: a missing required field is reported with the exact row number."""
    row = {"id": "T011", "date": "2026-02-02", "kind": "expense", "amount": "10"}

    raised = False
    message = ""
    try:
        build_transaction(row, row_number=5)
    except ValueError as exc:
        raised = True
        message = str(exc)

    assert raised
    assert message == "Row 5: missing required field 'category'."


def test_build_transaction_reports_non_numeric_amount():
    """Boundary: a non-numeric amount is reported instead of silently being dropped."""
    row = {"id": "T012", "date": "2026-02-03", "kind": "expense", "category": "food", "amount": "abc"}

    raised = False
    message = ""
    try:
        build_transaction(row, row_number=7)
    except ValueError as exc:
        raised = True
        message = str(exc)

    assert raised
    assert message == "Row 7: amount must be a number, got abc."
