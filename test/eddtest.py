'''
Created on 2017/02/12

@author: rindybell
'''
import unittest
from src.eddchars import EddChars


class Test(unittest.TestCase):

    def test_cost(self):
        eddchars = EddChars()
        self.assertEqual(eddchars.distance("play", "played"), 2)
        self.assertEqual(eddchars.distance("study", "studied"), 3)

        eddchars = EddChars(sub_cost=2.0)
        self.assertEqual(eddchars.distance("study", "studied"), 4)

if __name__ == "__main__":
    unittest.main()
