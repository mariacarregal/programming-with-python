# Design Rationale

Validation is split across two layers on purpose. `Transaction.__init__`
checks the domain invariants (amount must be positive, kind and category
must be known values) and raises before assigning anything, so an invalid
`Transaction` can never exist in memory no matter how it was built. One
level above, `validation.py` handles the messier job of turning raw,
external input -- a CSV row full of strings, or text typed at the CLI --
into clean data the constructor can accept, and attaches row-level context
(`"Row 8: amount must be a positive number, got -9.99"`) to whatever error
comes back. The effect is that the business rule for "what is a valid
amount" is written exactly once, inside `Transaction`, and both `storage.py`
and `cli.py` reuse the same `build_transaction` function instead of each
re-implementing their own checks -- so the CLI and the file loader can never
silently disagree about what counts as a valid transaction.
