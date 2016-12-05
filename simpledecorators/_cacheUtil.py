from threading import RLock


class _LockUnit(object):
    lockCount = 0

    def __init__(self):
        self.incLock = RLock()
        self.lock = RLock()
        super(_LockUnit, self).__init__()

    def incLockCount(self):
        self.incLock.acquire()
        try:
            self.lockCount += 1
            return self.lockCount
        finally:
            self.incLock.release()

    def decLockCount(self):
        self.incLock.acquire()
        try:
            self.lockCount -= 1
            return self.lockCount
        finally:
            self.incLock.release()

    def acquire(self):
        self.lock.acquire()

    def release(self):
        self.lock.release()


class KeyLock(object):
    def __init__(self):
        self.lock = RLock()
        self.locks = {}  # @type: _LockUnit

    def _getLockByKey(self, key):
        # type: (str) -> _LockUnit
        self.lock.acquire()
        try:
            if key not in self.locks:
                self.locks[key] = _LockUnit()
            return self.locks[key]
        finally:
            self.lock.release()

    def acquire(self, key):
        self.lock.acquire()
        try:
            lock = self._getLockByKey(key)
            count = lock.incLockCount()
        finally:
            self.lock.release()
        lock.acquire()
        return count

    def release(self, key):
        self.lock.acquire()
        lock = self._getLockByKey(key)
        if not lock.decLockCount():
            del self.locks[key]
        lock.release()
        self.lock.release()
