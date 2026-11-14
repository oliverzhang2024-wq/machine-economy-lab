from solution import invoice_totals
from decimal import Decimal
p={'m': {'input':'2','cached_input':'0.5','output':'8'}}
e=[{'account':'a','model':'m','input_tokens':1000000,'cached_input_tokens':500000,'output_tokens':1000000}]
assert invoice_totals(e,p)['a'] == Decimal('9.2500')
print('Example passed')
