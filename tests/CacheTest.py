import unittest

from simpledecorators.Cache import Cache, TimeCacheStorage

called = 0
class SafeTest(unittest.TestCase):
    def test_AddToCache(self):
        global called
        called = 0
        @Cache(cacheStorage=TimeCacheStorage(time_seconds=1, maxCount=1000))
        def func1(a,b,c):
            global called
            called += 1
            return a + b + c

        a = func1(1, 2, 3)
        b = func1(1, 2, 3)
        c = func1(1, 2, 3)
        d = func1(1, 2, 3)
        self.assertEqual(a, 1 + 2 + 3)
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(c, d)
        self.assertEqual(called, 1)

    def test_ReturnsNone(self):
        global called
        called = 0

        @Cache(cacheStorage=TimeCacheStorage(time_seconds=1, maxCount=1000))
        def func1(a, b, c):
            global called
            called += 1
            return None

        a = func1(1, 2, 3)
        b = func1(1, 2, 3)
        c = func1(1, 2, 3)
        d = func1(1, 2, 3)
        self.assertEqual(a, None)
        self.assertEqual(a, b)
        self.assertEqual(b, c)
        self.assertEqual(c, d)
        self.assertEqual(called, 1)

    def test_sameArguments(self):
        @Cache()
        def func1(a, b, c):
            return 1

        @Cache()
        def func2(a, b, c):
            return 2

        a = func1(1, 2, 3)
        b = func2(1, 2, 3)
        self.assertEqual(a, 1)
        self.assertEqual(b, 2)



if __name__ == "__main__":
    unittest.main()
