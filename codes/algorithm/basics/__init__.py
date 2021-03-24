# -*- coding: utf-8 -*-

# ===================================
# file_name     : __init__.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/11/7 10:59
# ide_name      : PyCharm
# project_name  : 4U
# ===================================

# max gong yue shu
def gys(x: int, y: int) -> int:
    if not y:
        return x
    return gys(y, x % y)


# print(gys(6, 12))


class MyNode(object):
    def __init__(self, value, next_node=None):
        self._value = value
        self._next = next_node

    @property
    def value(self):
        return self._value

    @property
    def next(self):
        return self._next


class MyTree(object):
    def __init__(self, value, left=None, right=None):
        self._value = value
        self._left = left
        self._right = right

    @property
    def value(self):
        return self._value

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right
