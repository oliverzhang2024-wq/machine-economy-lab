def _nonnegative_int(v):
    return type(v) is int and v >= 0

def settle_transfers(balances, transfers):
    if not all(_nonnegative_int(v) for v in balances.values()):
        raise ValueError('bad balance')
    result = balances.copy()
    seen = {}
    statuses = []
    for t in transfers:
        key = t['id']
        values = (t['from'], t['to'], t['amount'])
        if key in seen:
            if seen[key] != values:
                raise ValueError('conflicting transaction id')
            statuses.append('duplicate')
            continue
        sender, receiver, amount = values
        if sender not in result or receiver not in result:
            raise KeyError('unknown account')
        if sender == receiver or type(amount) is not int or amount <= 0:
            raise ValueError('invalid transfer')
        seen[key] = values
        if result[sender] < amount:
            statuses.append('insufficient_funds')
        else:
            result[sender] -= amount
            result[receiver] += amount
            statuses.append('settled')
    return result, statuses
