'''
Created on 2017/02/12

@author: rindybell
'''
import unittest
import src.eddchars


class Test(unittest.TestCase):

    def __init__(self):
        self.eddchars = src.eddchars.EddChars()

    def test_cost(self):
        self.assertEqual(self.eddchars.distance("played", "play"), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
