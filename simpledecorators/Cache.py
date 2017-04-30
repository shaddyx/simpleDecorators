#import time
from functools import wraps
from threading import RLock

import cachetools
import logging
import os
import json
import time
from abc import ABCMeta, abstractmethod, abstractproperty
logger = logging.getLogger('Cache')

def __defaultKeyCalculator(fn, args, kwargs):
    if hasattr(fn, "__self__"):
        clazz = fn.__self__.__class__
    else:
        clazz = ""
    return "{module}_{clazz}{name}{args}{kwargs}".format(clazz=clazz,name=fn.__name__, args=args, kwargs=kwargs, module=fn.__module__)

class CacheStorage:
    @abstractmethod
    def add(self, key, value):
        """
        method to add value to cache
        :param key: string key to store element to cache
        :param value: Objec
        """

    @abstractmethod
    def hasKey(self, key):
        """
        :param key: String key
        :return: True if key exists in cache
        :rtype: bool
        """
    @abstractmethod
    def get(self, key):
        """
        :param key:
        :return: value from cache, or raises KeyError if element not in cache
        """

class TimeCacheStorage(CacheStorage):
    def __init__(self, time_seconds=-1, maxCount=-1):
        """
        :type time_seconds: int
        :param time_seconds: time to live in cache (infinite if default)
        :type maxCount: int
        :param maxCount: maximum items in cache (infinite if default)
        """
        if time_seconds == -1:
            time_seconds = 9223372036854775807
        if maxCount == -1:
            maxCount = 9223372036854775807
        self.time_seconds = time_seconds
        self.maxCount = maxCount
        self.__storage = cachetools.TTLCache(maxsize=maxCount, ttl=time_seconds)

    def hasKey(self, key):
        return self.__storage.has_key(key)

    def add(self, key, value):
        self.__storage[key]=value

    def get(self, key):
        return self.__storage[key]
lock=RLock()
class FileCacheStorage(CacheStorage):
        def __init__(self, path):
            self.path=path
            lock.acquire()
            try:
                if not os.path.exists(path):
                    os.makedirs(path)
            finally:
                lock.release()

        def ___filePath(self, key):
            return os.path.join(self.path, key)

        def __serialize(self, data):
            return json.dumps(data)

        def __deSerialize(self, data):
            return json.loads(data)

        def hasKey(self, key):
            return os.path.exists(self.___filePath(key))

        def add(self, key, value):
            lock.acquire()
            try:
                f=open(self.___filePath(key), "w")
                f.write(self.__serialize(value))
                f.close()
            finally:
                lock.release()

        def get(self, key):
            lock.acquire()
            try:
                if not self.hasKey(key):
                    raise KeyError("No such key:", key)
                f = open(self.___filePath(key), "r")
                data = self.__deSerialize(f.read())
                f.close()
                return data
            finally:
                lock.release()




# noinspection PyPep8Naming
def Cache(
        cacheStorage=TimeCacheStorage(time_seconds=1, maxCount=1000),
        checkPutToCache=lambda key, res, args, kwargs: True,
        calcKey = __defaultKeyCalculator,
        log = False
    ):
    """
    :param cacheStorage: this parameter need to be implementation of CacheStorage, or factory method for this type
    :param checkPutToCache: this function calls after value from main function is get to determine is storing to cache needed, it must be a function with arguments: (key, functionResult, args, kwargs)
    :param calcKey: function to calculate the key, by default using function return str(args) + "_" + str(kwargs)
    :param log: turn on logging if true, by default is off
    :type log: bool
    :return:
    """
    if type(cacheStorage).__name__ == "function":
        cacheStorage = cacheStorage()
    def decorator(fn):
        def addToCache(key, args, kwargs):
            res = fn(*args, **kwargs)
            if (checkPutToCache(key, res, args, kwargs)):
                cacheStorage.add(key, res)
                if log:
                    logger.debug("Adding to cache by key:" + key)
            return res

        @wraps(fn)
        def wrapped(*args, **kwargs):
            key = calcKey(fn, args, kwargs)
            try:
                return cacheStorage.get(key)
            except KeyError:
                return addToCache(key, args, kwargs)
        return wrapped
    return decorator

if __name__=="__main__":
    @Cache(TimeCacheStorage(10, 1000))
    def cachedFunc(aa=0, bb=-1):
        print("Cached funcion called")
        return aa + bb

    @Cache(FileCacheStorage("../test"))
    def cachedFunc1(aa=0, bb=-1):
        print("Cached funcion called")
        return aa + bb

    for x in xrange(1, 1000):
        res = cachedFunc(aa=1, bb=2)
        assert res == 3
        res = cachedFunc1(aa=1, bb=2)
        assert res == 3
    for x in xrange(1, 1000):
        res = cachedFunc(2, 2)
        assert res == 4
        res = cachedFunc1(2, 2)
        assert res == 4
    time.sleep(2)
    for x in xrange(1, 1000):
        res = cachedFunc(aa=3, bb=2)
        assert res == 5
        res = cachedFunc1(aa=3, bb=2)
        assert res == 5
    for x in xrange(1, 1000):
        res = cachedFunc(1, 2)
        assert res == 3
        res = cachedFunc1(1, 2)
        assert res == 3
    time.sleep(2)
    for x in xrange(1, 1000):
        res = cachedFunc(aa=1, bb=2)
        assert res == 3
        res = cachedFunc1(aa=1, bb=2)
        assert res == 3
    for x in xrange(1, 1000):
         res = cachedFunc(1, x)
         assert res == 1 + x, "result is:" + str(res)
         res = cachedFunc1(1, x)
         assert res == 1 + x, "result is:" + str(res)

    from shutil import rmtree
    rmtree('../test')