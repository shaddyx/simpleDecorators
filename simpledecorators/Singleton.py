import functools
def Singleton(cls):

    # TODO: make the true singleton

    instance = cls()
    instance.__call__ = lambda: instance
    return instance


if __name__ == "__main__":
    @Singleton
    class TestClass:
        def __init__(self):
            print ("constructor called")

    print ("starting")

    a = TestClass()
    b = TestClass()
    #assert isinstance(a, TestClass), "Class is not instance of TestClass"
    assert a == b, "Classes are different"
