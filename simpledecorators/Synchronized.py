from threading import RLock


def Synchronized(lock=None):
    if not lock:
        lock=RLock()
    def decorator(fn):
        def wrapped(*args, **kwargs):
            lock.acquire()
            try:
                return fn(*args, **kwargs)
            finally:
                lock.release()

        return wrapped

    return decorator
