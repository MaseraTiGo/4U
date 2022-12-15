# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/10/26 16:50
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import abc


class A(abc.ABC):
    M = {}
    _N = None

    @classmethod
    def add(cls, apis):
        cls._N = cls._N if cls._N else {}
        cls._N[apis] = apis


class B(A):
    ...


class C(A):
    ...


B.add(1)
print(B._N)
C.add(2)
print(B._N)
print(C._N)
