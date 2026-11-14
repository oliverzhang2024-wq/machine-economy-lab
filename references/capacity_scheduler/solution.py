def _int(v): return type(v) is int

def allocate(jobs, workers):
    if len({j['id'] for j in jobs}) != len(jobs) or len({w['id'] for w in workers}) != len(workers):
        raise ValueError('duplicate ids')
    if any(not _int(j['units']) or j['units']<=0 or not _int(j['priority']) for j in jobs):
        raise ValueError('invalid job')
    if any(not _int(w['capacity']) or w['capacity']<0 or not _int(w['unit_cost']) or w['unit_cost']<0 for w in workers):
        raise ValueError('invalid worker')
    remaining={w['id']:w['capacity'] for w in workers}
    result={}
    for j in sorted(jobs,key=lambda x:(-x['priority'],x['id'])):
        eligible=[w for w in workers if j['skill'] in w['skills'] and remaining[w['id']] >= j['units']]
        if eligible:
            chosen=min(eligible,key=lambda w:(w['unit_cost'],w['id']))
            remaining[chosen['id']] -= j['units']
            result[j['id']] = chosen['id']
        else:
            result[j['id']] = None
    return result
