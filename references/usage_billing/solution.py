from decimal import Decimal, ROUND_HALF_UP

def invoice_totals(events, prices):
    totals = {}
    for e in events:
        inp, cached, out = (e[k] for k in ('input_tokens','cached_input_tokens','output_tokens'))
        if min(inp, cached, out) < 0 or cached > inp:
            raise ValueError('invalid token counts')
        p = prices[e['model']]
        cost = ((Decimal(inp-cached)*Decimal(str(p['input'])))+
                (Decimal(cached)*Decimal(str(p['cached_input'])))+
                (Decimal(out)*Decimal(str(p['output']))))/Decimal(1000000)
        totals[e['account']] = totals.get(e['account'], Decimal(0)) + cost
    return {a: total.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP) for a,total in totals.items()}
