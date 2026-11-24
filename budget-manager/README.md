# Personal Budget Manager

A command-line tool to add, list, and report income/expense transactions,
with validation at every entry point and persistence to a CSV file.

## Setup

Requires Python 3.10+. No external dependencies for the app itself;
`pytest` is only needed to run the test suite.

```bash
pip install pytest
```

## Run

From the `budget-manager/` folder:

```bash
cd src
python -m budget_manager.cli
```

This opens an interactive menu:

```
1. Add transaction
2. List transactions
3. Report
4. Save to file
5. Load from file
6. Quit
```

## Example

Loading the bundled sample data and asking for a report:

```
Choose an option: 5
path [data/sample_transactions.csv]:
Loaded 6 transactions from data/sample_transactions.csv
  Skipped -> Row 8: amount must be a positive number, got -9.99
  Skipped -> Row 9: category must be one of ['food', 'leisure', 'other', 'rent', 'salary', 'transport'], got crypto
  Skipped -> Row 10: duplicate id 'T002', skipped.

Choose an option: 3
Transactions: 6
Income:       2300.00
Expense:      715.80
Balance:      1584.20
```

`data/sample_transactions.csv` deliberately contains 3 broken rows (negative
amount, unknown category, duplicate id) to show that bad rows are reported
and skipped instead of crashing the load or silently corrupting totals.

Adding a transaction by hand:

```
Choose an option: 1
id: T100
date (YYYY-MM-DD): 2026-02-10
kind (expense/income): expense
category: food
amount: 12.40
currency [EUR]:
Added: [T100] 2026-02-10 food -12.40 EUR
```

## Test

From the `budget-manager/` folder:

```bash
python -m pytest
```

8 tests: one normal case plus at least two boundary cases for each of
`models.py`, `validation.py`, and `storage.py` (positive construction,
rejected negative/unknown-category input, dirty-input cleanup, missing
fields, non-numeric amounts, and a save/load round-trip with invalid and
duplicate rows).

## Known limitations

- Single in-memory budget per CLI session: no multi-user support, no undo
  (see the stretch challenge in the practice brief).
- `save` overwrites the whole file directly; there is no atomic
  temp-file-then-replace write, so a crash mid-save could leave a corrupted
  CSV. Out of scope for Release 1.
- The CLI is menu-driven only; there are no non-interactive command-line
  flags for scripting.
- `date` is stored as a plain string with no calendar validation beyond
  being required (e.g. `2026-13-40` would be accepted).
