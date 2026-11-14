def reconcile(events):
    state={}
    for e in events:
        order_id, status, v, t = (e[k] for k in ('order_id','status','version','timestamp'))
        if type(v) is not int or v<0 or type(t) is not int:
            raise ValueError('invalid event')
        old=state.get(order_id)
        if old is None or (v,t)>(old['version'],old['timestamp']):
            state[order_id]={'status':status,'version':v,'timestamp':t}
        elif (v,t)==(old['version'],old['timestamp']) and status!=old['status']:
            raise ValueError('inconsistent event')
    return state
