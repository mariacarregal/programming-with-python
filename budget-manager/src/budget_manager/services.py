"""Budget logic: add, filter, and summarize transactions."""


class Budget:
    """Holds a list of Transaction objects and answers questions about them."""

    def __init__(self):
        self._transactions = []

    def add(self, transaction):
        self._transactions.append(transaction)

    def all(self):
        return list(self._transactions)

    def count(self):
        return len(self._transactions)

    def filter_by_category(self, category):
        return [t for t in self._transactions if t.category == category]

    def filter_by_kind(self, kind):
        return [t for t in self._transactions if t.kind == kind]

    def total_income(self):
        return sum(t.amount for t in self._transactions if t.kind == "income")

    def total_expense(self):
        return sum(t.amount for t in self._transactions if t.kind == "expense")

    def balance(self):
        return self.total_income() - self.total_expense()
