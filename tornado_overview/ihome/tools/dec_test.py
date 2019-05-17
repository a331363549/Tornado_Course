# 裝飾器

import time
import functools


def time_dec(func):
    print("dec started")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print("last_time:{}".format(end_time - start_time))

    return wrapper


@time_dec
def add(a, b):
    time.sleep(3)
    return a + b


if __name__ == '__main__':
    add(1, 3)
