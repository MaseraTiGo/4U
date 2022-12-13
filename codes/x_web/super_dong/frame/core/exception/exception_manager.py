# -*- coding: utf-8 -*-
# @File    : exception_manager
# @Project : djangoProject
# @Time    : 2022/10/13 16:21
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from functools import wraps
from pprint import pprint


class T:
    ...


def my_trace(frame, event, arg):
    print()
    print(f"{'enter':*^188}")
    pprint(frame.f_locals.items())
    print(f"{'exit':*^188}")
    print()


def wrapper(method):
    dante = T()
    dante.ctx = "fuck you"
    dante.info = ""
    dante.stats = 1

    @wraps(method)
    def inner(*args, **kwargs):
        kwargs.update({"dante": dante})
        method(*args, **kwargs)
        return {
            "ctx": dante.ctx,
            "info": dante.info,
            "stats": dante.stats
        }

    return inner


class Fuck(object):

    @classmethod
    @wrapper
    def test(cls, dante=None):
        dante.ctx = "cao ni ma"
        dante.info = "motherfucker"
        dante.stats = 0


if __name__ == '__main__':
    # print(Fuck.test())
    import pysnooper
    with pysnooper.snoop():
        for _ in range(10):
            print(_)
