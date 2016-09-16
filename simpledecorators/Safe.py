from functools import wraps


def Safe(exception=Exception):
    """safe function call (if function raises an exception) it will be ignored"""
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exception:
                pass
        return wrapped
    return decorator


