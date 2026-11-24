"""Command-line interaction: input/output and user prompts.

This module only asks for input and prints output. It never calculates
totals itself (that's services.py) and never touches files directly
(that's storage.py) -- it just calls into those two.
"""

from .services import Budget
from .storage import load_transactions, save_transactions
from .validation import build_transaction

DATA_FILE = "data/sample_transactions.csv"

MENU = """
1. Add transaction
2. List transactions
3. Report
4. Save to file
5. Load from file
6. Quit
"""


def ask(prompt):
    return input(prompt).strip()


def add_transaction(budget):
    row = {
        "id": ask("id: "),
        "date": ask("date (YYYY-MM-DD): "),
        "kind": ask("kind (expense/income): "),
        "category": ask("category: "),
        "amount": ask("amount: "),
        "currency": ask("currency [EUR]: ") or "EUR",
    }
    try:
        transaction = build_transaction(row)
    except ValueError as exc:
        print(f"Could not add transaction: {exc}")
        return
    budget.add(transaction)
    print("Added:", transaction.describe())


def list_transactions(budget):
    if budget.count() == 0:
        print("No transactions yet.")
        return
    for transaction in budget.all():
        print(transaction.describe())


def show_report(budget):
    print(f"Transactions: {budget.count()}")
    print(f"Income:       {budget.total_income():.2f}")
    print(f"Expense:      {budget.total_expense():.2f}")
    print(f"Balance:      {budget.balance():.2f}")


def save_to_file(budget):
    path = ask(f"path [{DATA_FILE}]: ") or DATA_FILE
    save_transactions(path, budget.all())
    print(f"Saved {budget.count()} transactions to {path}")


def load_from_file(budget):
    path = ask(f"path [{DATA_FILE}]: ") or DATA_FILE
    transactions, errors = load_transactions(path)
    for transaction in transactions:
        budget.add(transaction)
    print(f"Loaded {len(transactions)} transactions from {path}")
    for error in errors:
        print("  Skipped ->", error)


def run():
    budget = Budget()
    print("Personal Budget Manager")

    while True:
        print(MENU)
        choice = ask("Choose an option: ")

        if choice == "1":
            add_transaction(budget)
        elif choice == "2":
            list_transactions(budget)
        elif choice == "3":
            show_report(budget)
        elif choice == "4":
            save_to_file(budget)
        elif choice == "5":
            load_from_file(budget)
        elif choice == "6":
            break
        else:
            print(f"Unknown option: {choice}")


if __name__ == "__main__":
    run()
