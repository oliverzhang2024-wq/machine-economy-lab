# Task 06 — Out-of-order webhook reconciliation

Implement `reconcile(events)`.

- Each event is a dictionary: `order_id`, `status`, `version` (nonnegative integer), `timestamp` (integer).
- Webhook events may arrive out of order and be duplicated.
- For each order, retain the event with highest `version`; on equal versions choose the event with later `timestamp`.
- If version AND timestamp are identical but statuses differ, raise `ValueError` (inconsistent source event).
- Raise `ValueError` for invalid version or timestamp types (including booleans), or negative version.
- Return `dict[order_id] = {'status': ..., 'version': ..., 'timestamp': ...}`.
- Do not mutate input. Use only standard library.
