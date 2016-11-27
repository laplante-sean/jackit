'''
Run unittests for the program
'''

import unittest
import os

if __name__ == "__main__":
    test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(test_path)
    runner = unittest.TextTestRunner()
    runner.run(suite)
