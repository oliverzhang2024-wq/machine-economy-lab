import unittest
from solution import export_rows

class Tests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(export_rows([], ['a','b']), 'a,b\n')
    def test_order_and_missing(self):
        self.assertEqual(export_rows([{'b': 2, 'a': 0}, {'a': None}], ['b','a']), 'b,a\n2,0\n,\n')
    def test_escape(self):
        self.assertEqual(export_rows([{'a':'a"b', 'b':'x\ny'}], ['a','b']), 'a,b\n"a""b","x\ny"\n')
    def test_invalid(self):
        with self.assertRaises(ValueError): export_rows([], [])
        with self.assertRaises(ValueError): export_rows([], ['a','a'])
    def test_iterable(self):
        self.assertEqual(export_rows(({'x':i} for i in range(2)), ['x']), 'x\n0\n1\n')

if __name__ == '__main__': unittest.main()
