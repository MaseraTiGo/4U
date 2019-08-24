# -*- coding: utf-8 -*-
# file_name       : resub.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/8/24 10:25

import re

url = 'http://www.hdbss.com/article-list-id-6-page-3.html'

flag = 0


def add_or_not(fn):
    def wrapper_add_or_not(*args, **kwargs):
        res = fn(*args, **kwargs)
        global flag
        if flag == 1:
            flag -= 1
        else:
            flag += 1
            res = str(int(res) - 1)
        return res

    return wrapper_add_or_not


@add_or_not
def add_one(x):
    return str(int(x.group()) + 1)


# a = re.sub('(?P<num>\d+)', add_one, url)
# print('a===============>', a)
for i in range(10):
    print(i, '--------->', "\033[0;3%dm%s\033[0m" % (i, "FUCKYOU"))
