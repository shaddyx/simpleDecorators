from simpledecorators.Synchronized import Synchronized
import unittest
import time
from threading import Thread
import os

class FileToolsTest(unittest.TestCase):
    counter = 0
    def test_Synchronized(self):
        global count
        @Synchronized()
        def func1():
            self.counter += 1
            time.sleep(0.3)

        t1 = Thread(target=func1)
        t1.start()
        t2 = Thread(target=func1)
        t2.start()
        time.sleep(0.2)
        self.assertEqual(self.counter, 1)
        time.sleep(0.6)
        self.assertEqual(self.counter, 2)

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
