# Task 01 — Reliable CSV export

Implement `export_rows(rows, columns)` in `solution.py`.

- `rows` is an iterable of dictionaries; `columns` is an ordered list of field names.
- Return CSV text with a header row (even when there are no data rows).
- Preserve the given column order and row order.
- Missing fields and `None` become an empty cell. Numbers become text.
- Use RFC-style CSV quoting for commas, double quotes, and embedded newlines.
- Use `\n` as the line terminator, including the final line.
- Raise `ValueError` when columns is empty or contains duplicate field names.
- Use only the Python standard library.
