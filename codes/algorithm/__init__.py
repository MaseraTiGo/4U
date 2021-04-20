# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/23/2019 8:29 AM'

import inspect


def retrieve_name(*var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars]


def print_(*args):
    [print(f'dong --------------> {arg}') for arg in args]
