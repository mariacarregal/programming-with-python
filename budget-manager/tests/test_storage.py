from budget_manager.models import Transaction
from budget_manager.storage import load_transactions, save_transactions


def test_save_and_load_roundtrip(tmp_path):
    """Normal case: what you save is exactly what you get back when you load it."""
    path = tmp_path / "transactions.csv"
    original = [
        Transaction(id="T001", date="2026-03-01", kind="income", category="salary", amount=1500),
        Transaction(id="T002", date="2026-03-02", kind="expense", category="food", amount=40),
    ]

    save_transactions(path, original)
    loaded, errors = load_transactions(path)

    assert errors == []
    assert [t.to_dict() for t in loaded] == [t.to_dict() for t in original]


def test_load_skips_invalid_and_duplicate_rows(tmp_path):
    """Boundary: invalid and duplicate rows are skipped and reported, not crashed on."""
    path = tmp_path / "transactions.csv"
    path.write_text(
        "id,date,kind,category,amount,currency\n"
        "T001,2026-03-01,income,salary,1500,EUR\n"
        "T002,2026-03-02,expense,food,-40,EUR\n"
        "T001,2026-03-03,expense,transport,10,EUR\n",
        encoding="utf-8",
    )

    loaded, errors = load_transactions(path)

    assert [t.id for t in loaded] == ["T001"]
    assert len(errors) == 2
