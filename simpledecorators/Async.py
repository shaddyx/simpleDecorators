from threading import Thread

def Async(executor=None):
    """
    @type executor: ThreadPool
    """
    def asyncDecorator (func):
        def wrapped(*args, **kwargs):
            def threadWrapper():
                return func(*args, **kwargs)
            if not executor:
                thread = Thread(target=threadWrapper)
                thread.start()
            else:
                executor.add_task(threadWrapper)
        return wrapped
    return asyncDecorator



if __name__ == "__main__":
    from time import sleep
    from ThreadPool import *
    
    @Async(executor=ThreadPool(5))
    def func(a, b):
        print "func called"
        sleep(1)
        print "func exit:" + str(a)

    @Async()
    def funcWithoutExecutor(a):
        print a

    for x in xrange(1, 100):
        funcWithoutExecutor("noExecutor:" + str(x))


    for x in xrange(1, 100):
        func(x, 2)