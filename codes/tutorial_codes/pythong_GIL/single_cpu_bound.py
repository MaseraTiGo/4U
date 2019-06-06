# single_cpu_bound.py
import time

COUNT = 50_000_000


def count_down():
    global COUNT
    while COUNT > 0:
        COUNT -= 1


s = time.perf_counter()
count_down()
c = time.perf_counter() - s
print('time taken in seconds - >:', c)
