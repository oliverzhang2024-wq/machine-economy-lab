from solution import allocate
jobs=[{'id':'j','skill':'python','units':3,'priority':1}]
workers=[{'id':'w','skills':['python'],'capacity':4,'unit_cost':5}]
assert allocate(jobs,workers)=={'j':'w'}
print('Example passed')
