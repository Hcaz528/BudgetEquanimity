import datetime
import logging
import time
import functools


def log_in_file(log_name="logs", file_type="txt"):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with open(f"{log_name}.{file_type}", "a") as f:
                f.write("In "+__name__ + " | Called function \""+func.__name__+"\" with arguments: (" +
                        " ".join([str(arg) for arg in args]) + ") at " + str(datetime.datetime.now()) + "\n")
            val = func(*args, **kwargs)
            return val

        return wrapper
    return inner


def simple_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        before = time.time()
        func(*args, **kwargs)
        print("\nFunction took:", time.time() - before, "seconds\n")

    return wrapper


class Advanced_log:
    def __init__(self, fnc=None) -> None:
        self._fnc = fnc
        self._memory = []

    def __call__(self, log_name="logs", file_type="txt", *args, **kwargs):
        print("in here", log_name)

        @functools.wraps(self._fnc)
        def inner(*args, **kwargs):
            print("in here")
            retval = self._fnc(*args, **kwargs)
            with open(f"{log_name}.{file_type}", "a") as f:
                f.write("In "+__name__ + " | Called function \""+self._fnc.__name__+"\" with arguments: (" +
                        " ".join([str(arg) for arg in args]) + ") at " + str(datetime.datetime.now()) + "\n")
            self._memory.append(retval)
            return retval

        return inner()

    def memory(self):
        return self._memory
