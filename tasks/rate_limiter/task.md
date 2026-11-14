# Task 03 — Sliding-window rate limiter

Implement `decide_requests(requests, limit, window_seconds)`.

- `requests` is a time-ordered list of `(timestamp, user_id)` pairs (timestamp in integer seconds).
- Return a list of booleans indicating whether each request is allowed.
- Each user may have at most `limit` ACCEPTED requests with timestamps in `(current_time - window_seconds, current_time]`.
- Rejected requests do not consume allowance. Users are independent.
- Raise `ValueError` when limit or window_seconds is nonpositive.
- Raise `ValueError` if timestamps decrease (equal timestamps are allowed).
- Use only the standard library.
