import time
from multiprocessing import Process, Manager

COUNT = 50_000_000


def count_down(e, pro_name):
    while e['count'] > 0:
        e['count'] -= 1
        print(pro_name, e['count'])


if __name__ == '__main__':
    s = time.perf_counter()
    with Manager() as manager:
        d = manager.dict()
        d['count'] = COUNT
        p1 = Process(target=count_down, args=(d, 'pro1--->'))
        p2 = Process(target=count_down, args=(d, 'pro2--->'))
        p1.start()
        p2.start()
        p1.join(timeout=2)
        p2.join(timeout=2)
    c = time.perf_counter() - s
    print('time taken in seconds - >:', c)
