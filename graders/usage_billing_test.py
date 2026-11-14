import unittest
from decimal import Decimal
from solution import invoice_totals
P={'cheap':{'input':'1.5','cached_input':'0.2','output':'4'},'exp':{'input':'6','cached_input':'1.5','output':'12'}}
def E(account='a', model='cheap', i=0, c=0, o=0):
    return dict(account=account,model=model,input_tokens=i,cached_input_tokens=c,output_tokens=o)

class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(invoice_totals([],P),{})
    def test_cached_not_double_counted(self):
        self.assertEqual(invoice_totals([E(i=1000000,c=800000,o=1000000)],P),{'a':Decimal('4.4600')})
    def test_aggregate_before_rounding(self):
        self.assertEqual(invoice_totals([E(i=11),E(i=11)],P),{'a':Decimal('0.0000')})
        self.assertEqual(invoice_totals([E(i=50000),E(i=50000)],P),{'a':Decimal('0.1500')})
    def test_multiple_accounts(self):
        self.assertEqual(invoice_totals([E('b','exp',1000000,0,500000),E('a','cheap',0,0,500000)],P),{'b':Decimal('12.0000'),'a':Decimal('2.0000')})
    def test_bad_counts(self):
        with self.assertRaises(ValueError): invoice_totals([E(i=4,c=5)],P)
        with self.assertRaises(ValueError): invoice_totals([E(o=-1)],P)
    def test_unknown_model(self):
        with self.assertRaises(KeyError): invoice_totals([E(model='nonexistent')],P)

if __name__ == '__main__': unittest.main()
