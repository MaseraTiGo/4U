# from concurrent.futures import ThreadPoolExecutor
import time
import threading

ref_count = 0
a_list = [i for i in range(100)]


def increase(thread_name):
    global a_list
    while a_list:
        print(thread_name, a_list.pop())


if __name__ == '__main__':
    t1 = threading.Thread(target=increase, args=('thread1--->',))
    t2 = threading.Thread(target=increase, args=('thread2--->',))
    t1.setDaemon(daemonic=True)
    t2.setDaemon(daemonic=True)
    t1.start()
    t2.start()
    t1.join(timeout=3)
    t2.join(timeout=3)

    print('--------end-------------')
