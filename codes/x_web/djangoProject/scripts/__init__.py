import threading
import time


def inner():
    print(f"dong ----------------> inner thread id: {threading.get_ident()}")
    print("\n孙子线程开始执行")
    print(f"\n父王线程222 id:{threading.main_thread().ident}")
    time.sleep(3)
    print("\n孙子线程执行结束")


def worker():
    print("\n子线程开始执行")
    time.sleep(1)
    print(f"\n父线程111 id:{threading.main_thread().ident}")
    time.sleep(3)
    print("\n子线程执行结束")


def main_thread():
    print(f"dong ----------------> main thread id: {threading.get_ident()}")
    t = threading.Thread(target=worker)
    print(f"dong ------------------> t1 :{t.ident}")
    t.start()
    print(f"dong ------------------> t2 :{t.ident}")
    # time.sleep(1)
    # print("\n主线程正在运行")
    # print("\n当前线程中的子线程：")
    # for sub_thread in threading.enumerate():
    #     if sub_thread.ident not in [threading.get_ident(), None]:
    #         print("\n子线程 {} 存活状态：{}".format(sub_thread.ident,
    #                                       sub_thread.is_alive()))


if __name__ == "__main__":
    main_thread()
