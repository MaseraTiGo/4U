# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '5/16/2019 8:23 PM'

import time
from functools import wraps


class TimeCount(object):
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        @wraps(func)
        def indoor(*args, **kwargs):
            s = time.time()
            func(*args, **kwargs)
            print('the fucking cost time is:', time.time() - s)

        print('your name is', self.name)
        return indoor


class FuckingTest(object):
    @TimeCount('dante')
    def test(self):
        for i in range(3):
            time.sleep(1)


fuck = FuckingTest()
fuck.test()
print(fuck.test)
# import wrapt
# @wrapt.decorator()