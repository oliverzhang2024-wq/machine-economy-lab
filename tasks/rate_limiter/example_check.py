from solution import decide_requests
assert decide_requests([(0,'a'),(1,'a'),(2,'a'),(11,'a')], 2, 10) == [True,True,False,True]
print('Example passed')
