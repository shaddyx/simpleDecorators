import threading
import unittest

import time

from simpledecorators import _cacheUtil
from simpledecorators.Cache import Cache, TimeCacheStorage

called = 0
acq1=False
acq2=False
class CacheUtilTest(unittest.TestCase):
    # def test_2_diff_locks(self):
    #     kLock = _cacheUtil.KeyLock()
    #     kLock.acquire("key1")
    #
    #     def thr2():
    #         print ("started thread")
    #         kLock.acquire("key2")
    #         print ("lock acquired")
    #     thr = threading.Thread(target=thr2)
    #     thr.run()
    #     time.sleep(1)

    def test_2_locks(self):
        global acq1, acq2
        kLock = _cacheUtil.KeyLock()
        kLock.acquire("key1")
        acq1 = True
        time.sleep(0.5)
        def thr2():
            global  acq2
            kLock.acquire("key1")
            self.assertFalse(acq1)
            acq2 = True
            kLock.release("key1")

        thr = threading.Thread(target=thr2)
        thr.start()
        time.sleep(1)
        acq1 = False
        kLock.release("key1")
        time.sleep(0.3)
        self.assertTrue(acq2)


if __name__ == "__main__":
    unittest.main()
