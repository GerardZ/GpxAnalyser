import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from myOpenStreetMap import *

class TestMyCode(unittest.TestCase):

    def test_getCenterCoordinate(self):
        # check multiple values
        coordinates = [(50,15),(20,20),(30,10)]
        resultCoordinate = getCenterCoordinate(coordinates)
        self.assertEqual(resultCoordinate, (35.0,15.0))

        # check going over meridian
        coordinates = [(15,-178),(15,179)]
        resultCoordinate = getCenterCoordinate(coordinates)
        self.assertEqual(resultCoordinate, (15.0, -179.5))

if __name__ == '__main__':
    unittest.main()