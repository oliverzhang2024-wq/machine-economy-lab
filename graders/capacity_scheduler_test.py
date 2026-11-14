import unittest,copy
from solution import allocate
def J(i, skill='python', units=1, priority=0): return {'id':i,'skill':skill,'units':units,'priority':priority}
def W(i, skills=('python',), capacity=2, cost=10): return {'id':i,'skills':list(skills),'capacity':capacity,'unit_cost':cost}
class Tests(unittest.TestCase):
    def test_simple(self): self.assertEqual(allocate([J('j')],[W('w')]),{'j':'w'})
    def test_tie_break(self): self.assertEqual(allocate([J('j')],[W('z',cost=3),W('a',cost=3)]),{'j':'a'})
    def test_priority_and_capacity(self):
        self.assertEqual(allocate([J('low',units=2,priority=1),J('high',units=1,priority=2)],[W('cheap',capacity=2,cost=1),W('exp',capacity=2,cost=5)]),{'high':'cheap','low':'exp'})
    def test_no_split(self): self.assertEqual(allocate([J('j',units=3)],[W('a',capacity=2),W('b',capacity=2)]),{'j':None})
    def test_skill(self): self.assertEqual(allocate([J('a','ml'),J('b')],[W('only_python')]),{'a':None,'b':'only_python'})
    def test_immutable(self):
        jobs=[J('a')];workers=[W('w')]; a=copy.deepcopy((jobs,workers));allocate(jobs,workers);self.assertEqual((jobs,workers),a)
    def test_invalid(self):
        with self.assertRaises(ValueError): allocate([J('x'),J('x')],[W('w')])
        with self.assertRaises(ValueError): allocate([J('x')],[W('w'),W('w')])
        with self.assertRaises(ValueError): allocate([J('x',units=0)],[W('w')])
        with self.assertRaises(ValueError): allocate([J('x')],[W('w',capacity=-1)])

if __name__ == '__main__': unittest.main()
