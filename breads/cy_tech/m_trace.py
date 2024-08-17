# -*- coding: utf-8 -*-
# @File    : m_trace
# @Project : 4U
# @Time    : 2024/8/16 15:47
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import inspect
import logging
from functools import wraps

logging.basicConfig(filename='import_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')


def log_import(fn=None):
    stack = inspect.stack()
    call_order = [
                     x.filename for x in stack[2:] if
                     not x.filename.startswith('<')
                 ][::-1]
    calling_module = inspect.getmodule(stack[1][0])

    if calling_module:
        module_name = calling_module.__name__
    else:
        module_name = 'Unknown'

    obj_name = '.' + fn.__name__ if fn else ''
    msg = f'Module <{module_name}{obj_name}> imported by \n'
    for i, filename in enumerate(call_order):
        msg += f'{" " * 26}{" " * 2 * i}\_{filename}\n'
    logging.info(msg)

    if fn is None:
        return

    @wraps(fn)
    def inner(*args, **kwargs):
        return fn(*args, **kwargs)

    return inner


log_import()


@log_import
def holy_shit():
    print("hello, motherfucker")
