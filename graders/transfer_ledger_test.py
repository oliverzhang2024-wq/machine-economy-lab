import unittest
from solution import settle_transfers
def T(i='x',src='a',dst='b',amt=3): return {'id':i,'from':src,'to':dst,'amount':amt}
class Tests(unittest.TestCase):
    def test_basic_and_does_not_mutate(self):
        b={'a':10,'b':0}
        self.assertEqual(settle_transfers(b,[T(),T('y','b','a',1)]),({'a':8,'b':2},['settled','settled']))
        self.assertEqual(b,{'a':10,'b':0})
    def test_duplicate(self): self.assertEqual(settle_transfers({'a':10,'b':0},[T(),T()]),({'a':7,'b':3},['settled','duplicate']))
    def test_insufficient_idempotent(self):
        t=[T('x',amt=9),T('y','b','a',12),T('x',amt=9)]
        self.assertEqual(settle_transfers({'a':2,'b':20},t),({'a':14,'b':8},['insufficient_funds','settled','duplicate']))
    def test_conflicting_id(self):
        with self.assertRaises(ValueError): settle_transfers({'a':10,'b':0},[T(),T(amt=4)])
    def test_bad_amount(self):
        for v in (0,-1,True,1.2):
            with self.assertRaises(ValueError): settle_transfers({'a':10,'b':0},[T(amt=v)])
    def test_bad_accounts(self):
        with self.assertRaises(KeyError): settle_transfers({'a':10},[T()])
        with self.assertRaises(ValueError): settle_transfers({'a':10,'b':0},[T(src='a',dst='a')])
        with self.assertRaises(ValueError): settle_transfers({'a':-1,'b':0},[])

if __name__ == '__main__': unittest.main()
