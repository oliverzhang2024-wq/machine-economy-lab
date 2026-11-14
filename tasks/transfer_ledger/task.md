# Task 04 — Idempotent transfer ledger

Implement `settle_transfers(balances, transfers)`.

- `balances` maps account IDs to integer cents (nonnegative). Do not mutate it.
- Each transfer has: `id`, `from`, `to`, `amount` (strictly positive integer cents).
- Apply transfers in sequence. Return `(new_balances, statuses)`.
- Statuses are `settled`, `duplicate`, or `insufficient_funds`.
- A repeated transfer ID with EXACTLY the same from/to/amount must return `duplicate` and never pay twice, even if the first attempt had insufficient funds.
- Reusing an ID with different details raises `ValueError`.
- Unknown accounts raise `KeyError`, self-transfers raise `ValueError`.
- Invalid balances or amounts (negative, noninteger, boolean, or zero amount) raise `ValueError`.
- Use only standard library.
