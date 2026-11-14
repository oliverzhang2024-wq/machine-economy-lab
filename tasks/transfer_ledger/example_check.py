from solution import settle_transfers
t=[{'id':'t1','from':'a','to':'b','amount':5},{'id':'t1','from':'a','to':'b','amount':5}]
assert settle_transfers({'a':10,'b':0},t)==({'a':5,'b':5},['settled','duplicate'])
print('Example passed')
