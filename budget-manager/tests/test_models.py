from budget_manager.models import Transaction


def test_create_valid_transaction():
    """Normal case: a well-formed transaction is accepted and stores the right values."""
    t = Transaction(id="T001", date="2026-01-15", kind="expense", category="food", amount=18.5)

    assert t.id == "T001"
    assert t.kind == "expense"
    assert t.category == "food"
    assert t.amount == 18.5
    assert t.currency == "EUR"


def test_rejects_non_positive_amount():
    """Boundary: amount must be strictly positive -- 0 and negative are both rejected."""
    for bad_amount in (0, -5):
        raised = False
        message = ""
        try:
            Transaction(id="T002", date="2026-01-15", kind="expense", category="food", amount=bad_amount)
        except ValueError as exc:
            raised = True
            message = str(exc)

        assert raised, f"amount={bad_amount} should have been rejected"
        assert message == f"amount must be a positive number, got {bad_amount}"


def test_rejects_unknown_category():
    """Boundary: category must be one of the controlled vocabulary values."""
    raised = False
    message = ""
    try:
        Transaction(id="T003", date="2026-01-15", kind="expense", category="crypto", amount=10)
    except ValueError as exc:
        raised = True
        message = str(exc)

    assert raised
    assert "crypto" in message
    assert "category must be one of" in message
