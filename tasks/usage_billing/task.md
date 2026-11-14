# Task 02 — Metered inference billing

Implement `invoice_totals(events, prices)` in `solution.py`.

- Each event has `account`, `model`, `input_tokens`, `cached_input_tokens`, `output_tokens`.
- `cached_input_tokens` is already INCLUDED in `input_tokens`; do not double charge it.
- `prices[model]` contains USD per million tokens: `input`, `cached_input`, `output`.
- Compute per-account total, summing UNROUNDED amounts across events.
- Return `dict[str, decimal.Decimal]`, with each total rounded to 4 decimal places using ROUND_HALF_UP.
- Reject negative token counts and cases where cached tokens exceed total input (`ValueError`).
- Reject unknown models (`KeyError`).
- Use Decimal arithmetic from string representations of rates; no floats for cost calculation.
- Use only the standard library.
