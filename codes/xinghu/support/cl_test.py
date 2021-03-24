# -*- coding: utf-8 -*-

# ===================================
# file_name     : cl_test.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/9/5 15:46
# ide_name      : PyCharm
# project_name  : xinghu
# ===================================

def test(a, ex=[]):
    ex.append(a)
    print(ex)


test(1)
test(2, ex=['a'])
test(3)
