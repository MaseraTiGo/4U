import time
from functools import wraps
from typing import List


def timer(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        s_time = time.time()
        result = fn(*args, **kwargs)
        duration = time.time() - s_time
        print(f"{duration}")
        return result

    return inner


@timer
def test():
    for _ in range(3):
        time.sleep(1)


def select_second(data: List[int]):
    if len(data) <= 1:
        return None

    if len(data) == 2:
        return min(data)

    max_ = max(data[:2])
    max_2 = min(data[:2])
    for item in data[2:]:
        if item >= max_:

            max_2 = max_

            max_ = item

        elif item > max_2:
            max_2 = item
    print(max_2)


if __name__ == '__main__':
    # test()
    data = [1]
    select_second(data)
