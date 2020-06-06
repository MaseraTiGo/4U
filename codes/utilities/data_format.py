# -*- coding: utf-8 -*-
# file_name       : data_format.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/5/1 16:32


class MyDict(object):
    def __init__(self, kwargs):
        self._kwargs = kwargs
        # super().__init__()
        if not isinstance(kwargs, dict):
            raise Exception('WRONG  DATA FORMAT')
        # else:
        #     self.handle(kwargs)

    # def handle(self, kwargs):
    #     for k, v in kwargs.items():
    #         setattr(self, k, v)

    def __getattr__(self, item):
        return self._kwargs[item]

    def __getitem__(self, item):
        return self._kwargs[item]


a = {'fuck': 'bullshit', 'you': 'stupid'}
# m = MyDict(a)
# print(m['fuck'])
# print(m.fuck)


