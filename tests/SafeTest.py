from simpledecorators.Safe import Safe
from simpledecorators.Synchronized import Synchronized
import unittest
import time
from threading import Thread
import os

class SafeTest(unittest.TestCase):
    def test_Safe(self):
        @Safe()
        def func1():
            raise Exception("test Exception")
        func1()
    def test_SafeRaises(self):
        @Safe(exception=NameError)
        def func1():
            raise RuntimeError("test Exception")
        try:
            func1()
        except RuntimeError as e:
            return
        raise Exception("Error")

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
