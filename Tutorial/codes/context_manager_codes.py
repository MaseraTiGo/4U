# -*- coding: utf-8 -*-
# file_name       : context_manager_codes.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/1/1 10:05


class MrDongSql(object):
    _names_list = []
    _default_prefix = 'mr_dong'
    _default_suffix = 0
    _data_dict = {'a': 'aston', 'b': 'bugatti', 'c': 'Cayenne', 'd': 'dante'}

    @classmethod
    def connect(cls, name=None):
        if not name:
            name = cls._default_prefix + str(cls._default_suffix)
            cls._default_suffix += 1
        elif name in cls._names_list:
            raise Exception('name duplicate, rename!')
        cls._names_list.append(name)
