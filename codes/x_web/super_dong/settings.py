# -*- coding: utf-8 -*-
# @File    : settings
# @Project : djangoProject
# @Time    : 2022/10/12 14:59
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import datetime


class MyMeta(type):
    def __str__(cls):
        return f'<[D0NG]> At: <[{datetime.datetime.now()}]> {"-" * 33}> '


class PRINT_PREFIX(metaclass=MyMeta):
    ...
