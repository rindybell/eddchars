'''
Created on 2017/02/12

@author: rindybell
'''
import unittest
from src.eddchars import EddChars


class Test(unittest.TestCase):

    def test_cost(self):
        self.eddchars = EddChars()
        self.assertEqual(self.eddchars.distance("played", "play"), 2)

if __name__ == "__main__":
    unittest.main()
