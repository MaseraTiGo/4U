import time
from threading import Thread

COUNT = 50_000_000


def count_down():
    global COUNT
    while COUNT > 0:
        COUNT -= 1


s = time.perf_counter()
t1 = Thread(target=count_down)
t2 = Thread(target=count_down)
t1.start()
t2.start()
t1.join()
t2.join()
c = time.perf_counter() - s
print('time taken in seconds - >:', c)
