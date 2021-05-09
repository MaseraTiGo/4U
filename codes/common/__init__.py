# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/23/2019 7:59 AM'

import time
import random


# generate random integer nums
def generate_nine_nums(start=0, end=100, nums=9):
    return random.choices(range(start, end), k=nums)


def time_statistics(fn):
    def inner(*args, **kwargs):
        s = time.time()
        fn(*args, **kwargs)
        print(f'dong ---------------> time cost: {time.time() - s}')

    return inner
