# -*- coding: utf-8 -*-
# @File    : attr
# @Project : x_web
# @Time    : 2023/1/6 11:00
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

prefix = 'dong ---------->'


class Descriptor(object):

    def __set_name__(self, owner, name):
        print(f"{prefix} set name: {name}")
        self._name = name

    def __get__(self, instance, owner):
        print(f"{prefix} get attr from __get__: {self._name}")
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        print(f"{prefix} set value from __set__: {value}")
        instance.__dict__[self._name] = value
        print(f'{prefix} not here __set__')


class Fuck(object):
    Desc = Descriptor()

    def __getattr__(self, item):
        print(f"dong ---------> get {item} from getattr")
        return "fuck you"

    def __getattribute__(self, item):
        print(f"dong ---------> get {item} from getattribute")
        # raise AttributeError
        if item == '__dict__':
            return {}
        return "motherfucker"
