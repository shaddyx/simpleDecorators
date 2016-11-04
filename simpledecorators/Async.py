from functools import wraps
from threading import Thread
class AsyncFuture(object):
    complete=False
    working=False
    error=None
    result=None

def Async(executor=None):
    """
    @type executor: simpledecorators.ThreadPool
    @rtype: AsyncFuture
    """
    def asyncDecorator (func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            future = AsyncFuture();
            def threadWrapper():
                future.working = True
                try:
                    future.result=func(*args, **kwargs)
                    future.complete = True
                except Exception as e:
                    future.error=True
                finally:
                    future.working=False
            if not executor:
                thread = Thread(target=threadWrapper)
                thread.daemon = True
                thread.start()
            else:
                executor.add_task(threadWrapper)
            return future
        return wrapped
    return asyncDecorator

if __name__ == "__main__":
    from time import sleep
    from ThreadPool import *
    try:
        xrange
    except NameError:
        xrange = range
    class TestClass():
        @Async()
        def testDecorated(self):
            print (345)
    testClass = TestClass()
    testClass.testDecorated()
    @Async(executor=ThreadPool(5))
    def func(a, b):
        print ("func called")
        sleep(1)
        print ("func exit:" + str(a))

    @Async()
    def funcWithoutExecutor(a):
        print (a)

    for x in xrange(1, 10):
        funcWithoutExecutor("noExecutor:" + str(x))


    for x in xrange(1, 15):
        func(x, 2)