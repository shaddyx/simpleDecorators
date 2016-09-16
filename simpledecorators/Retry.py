import time
from functools import wraps


def Retry(
        count,
        delay=None,
        exception=Exception
    ):
    """

    :param count: retry count
    :param delay: delay in seconds after each fail (if can be a function wich will calls after each fail (*args, **kwargs))
    :param exception: exception to wait (Exception by default)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            retries=count
            while True:
                try:
                    return fn(*args, **kwargs)
                except exception as e:
                    retries -= 1
                    if retries <= 0:
                        raise e
                    if delay:
                        if type(delay).__name__ == "function":
                            delay()
                        else:
                            time.sleep(delay)

        return wrapper
    return decorator

if __name__ == "__main__":
    count = 0
    delayCalled = 0
    def __delayFunc():
        global delayCalled
        delayCalled += 1

    @Retry(10, delay=__delayFunc)
    def func1(param, namedParam):
        global count
        count += 1
        print ("calling try:" + str(count))
        assert param == 3 and namedParam == 4, "parameters are not pass"
        if count < 8:
            raise Exception("aaa")
    func1(3, 4)

    assert count == 8
    assert delayCalled == 7, "Delay count must be count - 1"

    count = 0
    err = False
    @Retry(10, delay=0.2)
    def func2():
        global count
        count += 1
        raise Exception("aaa")
    try:
        func2()
    except:
        err = True
    assert count == 10
    assert err, "Error must be thrown"

    err=False
    count = 0
    @Retry(10, delay=0.2, exception=KeyError)
    def func2():
        global count
        count += 1
        raise Exception()
    try:
        func2()
    except:
        err = True
    assert count == 1, "Count must be only 1, but was:" + str(count)
