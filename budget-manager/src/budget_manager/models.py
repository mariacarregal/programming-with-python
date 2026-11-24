"""Transaction schema / domain model."""


class Transaction:
    """A single income or expense record.

    __init__ validates before assigning anything, so an invalid Transaction
    can never exist (same invariant as Wallet in the OOP notes).
    """

    ALLOWED_KINDS = {"expense", "income"}
    ALLOWED_CATEGORIES = {"food", "transport", "rent", "salary", "leisure", "other"}

    def __init__(self, id, date, kind, category, amount, currency="EUR"):
        if kind not in self.ALLOWED_KINDS:
            raise ValueError(f"kind must be one of {sorted(self.ALLOWED_KINDS)}, got {kind}")
        if category not in self.ALLOWED_CATEGORIES:
            raise ValueError(
                f"category must be one of {sorted(self.ALLOWED_CATEGORIES)}, got {category}"
            )
        if amount <= 0:
            raise ValueError(f"amount must be a positive number, got {amount}")

        self.id = id
        self.date = date
        self.kind = kind
        self.category = category
        self.amount = float(amount)
        self.currency = currency

    def describe(self):
        sign = "-" if self.kind == "expense" else "+"
        return f"[{self.id}] {self.date} {self.category} {sign}{self.amount:.2f} {self.currency}"

    @classmethod
    def from_dict(cls, row):
        """Alternate constructor, e.g. for rows coming from storage.py."""
        return cls(
            id=row["id"],
            date=row["date"],
            kind=row["kind"],
            category=row["category"],
            amount=row["amount"],
            currency=row.get("currency", "EUR"),
        )

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "kind": self.kind,
            "category": self.category,
            "amount": self.amount,
            "currency": self.currency,
        }
