from collections import defaultdict, deque

def decide_requests(requests, limit, window_seconds):
    if limit <= 0 or window_seconds <= 0:
        raise ValueError('positive bounds required')
    accepted = defaultdict(deque)
    result = []
    prev = None
    for ts, user in requests:
        if prev is not None and ts < prev:
            raise ValueError('events are not ordered')
        prev = ts
        q = accepted[user]
        while q and q[0] <= ts - window_seconds:
            q.popleft()
        allowed = len(q) < limit
        result.append(allowed)
        if allowed:
            q.append(ts)
    return result
