# -*- coding: utf-8 -*-
# @File    : cal
# @Project : djangoProject
# @Time    : 2022/10/17 10:27
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""


class Calculator(object):

    def __init__(self, default: int, progress=""):
        self._default = default
        self._progress = f"{self._default}" if not progress else progress

    def add(self, value: int):
        return Calculator(self._default + value, self._progress + f'+{value}')

    def sub(self, value: int):
        return Calculator(self._default - value, self._progress + f'-{value}')

    @property
    def result(self):
        return self._default

    @property
    def expr(self):
        return self._progress

    def __call__(self, *args, **kwargs):
        return self._default


# c = Calculator(2)
# d = c.add(2).add(3).sub(1)
# print(d.result)
# print(d.expr)
# e = d.sub(1).add(2)
# f = d.add(2).sub(1)
# print(e())
# print(e.expr)
# print(f())
# print(f.expr)


import pyzipper

secret_password = 'dante'

with pyzipper.AESZipFile('new_test.zip',
                         'w',
                         compression=pyzipper.ZIP_LZMA) as zf:
    zf.setpassword(secret_password.encode())
    zf.setencryption(pyzipper.WZ_AES, nbits=128)
    zf.write('cal.py', 'callal.py')
    zf.write('__init__.py', 'tini.py')
