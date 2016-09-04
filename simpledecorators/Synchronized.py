from threading import RLock


def Synchronized(arg):
    def decorator(fn):
        lock = RLock()
        def wrapped(*args, **kwargs):
            lock.acquire()
            try:
                return fn(*args, **kwargs)
            finally:
                lock.release()

        return wrapped

    return decorator
