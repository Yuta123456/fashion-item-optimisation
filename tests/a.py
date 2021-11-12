import unittest
import sys
import pathlib

currentdir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(currentdir)+"/../util/")
from util import *
from util_class import util_estimater
class TestUnilFunctions(unittest.TestCase):

    # def make_coodinates(select_items, item, layer):
    def test_make_coodinates(self):
        select_items = [["one", "two"], ["three"], ["four", "five", "six"]]
        item = "seven"
        layer = 2
        make_coodinates(select_items, item, layer)


    def test_score_estimater(self):
        estimater = util_estimater.ScoreEstimater()
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()