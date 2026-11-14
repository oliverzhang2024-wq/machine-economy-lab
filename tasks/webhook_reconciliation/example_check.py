from solution import reconcile
e=[{'order_id':'a','status':'paid','version':2,'timestamp':20}, {'order_id':'a','status':'new','version':1,'timestamp':30}]
assert reconcile(e)=={'a':{'status':'paid','version':2,'timestamp':20}}
print('Example passed')
