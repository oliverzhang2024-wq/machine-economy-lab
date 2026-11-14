import unittest
from solution import reconcile
def E(id='a',status='new',version=1,timestamp=10): return dict(order_id=id,status=status,version=version,timestamp=timestamp)
class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(reconcile([]),{})
    def test_version_over_timestamp(self): self.assertEqual(reconcile([E(version=3,timestamp=1,status='paid'),E(version=1,timestamp=100,status='new')])['a']['status'],'paid')
    def test_latest_same_version(self): self.assertEqual(reconcile([E(timestamp=20,status='paid'),E(timestamp=10,status='new')])['a']['status'],'paid')
    def test_duplicate(self): self.assertEqual(reconcile([E(),E(),E(id='b')]),{'a':{'status':'new','version':1,'timestamp':10},'b':{'status':'new','version':1,'timestamp':10}})
    def test_conflict(self):
        with self.assertRaises(ValueError): reconcile([E(status='paid'),E(status='new')])
    def test_invalid(self):
        for v in (-1,True,1.2):
            with self.assertRaises(ValueError): reconcile([E(version=v)])
        with self.assertRaises(ValueError): reconcile([E(timestamp=True)])

if __name__ == '__main__': unittest.main()
