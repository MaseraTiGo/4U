# -*- coding: utf-8 -*-
# @File    : events
# @Project : x_web
# @Time    : 2023/2/7 11:00
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import threading
import time

flag = False


def fuck_flag():
    return flag


def func_a(cv):
    with cv:
        cv.wait(timeout=1)
        print(f"dong -------------> fuck you aaa")


def func_b(cv):
    with cv:
        cv.wait(timeout=1)
        print(f"dong -------------> fuck you bbb")


if __name__ == '__main__':
    cv = threading.Condition()
    print("dong -------------> main thread")
    threading.Thread(target=func_b, args=(cv, )).start()
    threading.Thread(target=func_a, args=(cv, )).start()
    time.sleep(3)
    with cv:
        flag = True
        cv.notify_all()
