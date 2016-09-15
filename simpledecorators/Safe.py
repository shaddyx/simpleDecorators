def Safe(exception=Exception):
    """safe function call (if function raises an exception) it will be ignored"""
    def decorator(fn):
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except exception:
                pass
        wrapped.__name__ = fn.__name__ + "Retry_wrapped"
        return wrapped
    return decorator


