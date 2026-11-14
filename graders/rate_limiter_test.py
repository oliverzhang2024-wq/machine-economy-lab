import unittest
from solution import decide_requests
class Tests(unittest.TestCase):
    def test_empty(self): self.assertEqual(decide_requests([], 2, 10), [])
    def test_window_excludes_boundary(self):
        self.assertEqual(decide_requests([(0,'a'),(9,'a'),(10,'a')],2,10),[True,True,True])
    def test_rejection_not_counted(self):
        self.assertEqual(decide_requests([(0,'a'),(1,'a'),(2,'a'),(3,'a')],2,100),[True,True,False,False])
    def test_per_user(self):
        self.assertEqual(decide_requests([(0,'a'),(0,'b'),(1,'a'),(1,'b')],1,10),[True,True,False,False])
    def test_equal_timestamps(self):
        self.assertEqual(decide_requests([(0,'a'),(0,'a'),(0,'a')],2,10),[True,True,False])
    def test_invalid(self):
        with self.assertRaises(ValueError): decide_requests([],0,10)
        with self.assertRaises(ValueError): decide_requests([],1,0)
        with self.assertRaises(ValueError): decide_requests([(2,'a'),(1,'b')],1,10)

if __name__ == '__main__': unittest.main()
