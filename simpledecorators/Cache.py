import time
import heapq
import expiringdict
import logging
logger = logging.getLogger('Cache')
def timeCache(time_seconds=-1, maxCount=1000, checkPutToCache=lambda res, args, kwargs: True, log=False):
    if time_seconds == -1:
        time_seconds = 9223372036854775807
    if maxCount == -1:
        maxCount = 9223372036854775807
    def decorator(fn):
        cacheStorage = expiringdict.ExpiringDict(max_age_seconds=time_seconds, max_len=maxCount)
        def calcKey(*args, **kwargs):
            return str(args) + "_" + str(kwargs)

        def addToCache(*args, **kwargs):
            key = calcKey(*args, **kwargs)
            res = fn(*args, **kwargs)
            if (checkPutToCache(res, args, kwargs)):
                cacheStorage[key] = res
                if log:
                    logger.debug("Adding to cache by key:" + key)
            return res

        def decorated(*args, **kwargs):
            key = calcKey(*args, **kwargs)
            if not key in cacheStorage.keys():
                return addToCache(*args, **kwargs)
            else:
                try:
                    return cacheStorage[key]
                except KeyError:
                    return addToCache(*args, **kwargs)
        return decorated
    return decorator

if __name__=="__main__":
    @timeCache(1, maxCount=100)
    def cachedFunc(aa=0, bb=-1):
        print("Cached funcion called")
        return aa + bb
    for x in xrange(1, 1000):
        res = cachedFunc(aa=1, bb=2)
        assert res == 3
    for x in xrange(1, 1000):
        res = cachedFunc(2, 2)
    assert res == 4
    time.sleep(2)
    for x in xrange(1, 1000):
        res = cachedFunc(aa=3, bb=2)
        assert res == 5
    for x in xrange(1, 1000):
        res = cachedFunc(1, 2)
        assert res == 3
    time.sleep(2)
    for x in xrange(1, 1000):
        res = cachedFunc(aa=1, bb=2)
        assert res == 3
    for x in xrange(1, 1000):
        res = cachedFunc(1, x)
        assert res == 1 + x, "result is:" + str(res)
