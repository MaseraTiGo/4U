# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : x_web
# @Time    : 2022/12/13 14:53
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from django.db.models import QuerySet

from super_dong.frame.core.exception import DataError


class TearParts(object):

    def __init__(self, obj_list, cur_page, size=10):
        self.size = size
        self.cur_page = cur_page
        self.data = None

        if self.cur_page > 0:
            self(obj_list)
        else:
            raise DataError("文件页数要求大于0")

    def json(self):
        return {
            'total': self.total,
            'total_page': self.total_page,
            'size': self.size,
            'cur_page': self.cur_page,
        }

    def get_list(self):
        return self.data

    def __call__(self, obj_list):
        if isinstance(obj_list, QuerySet):
            self.total = obj_list.count()
        else:
            self.total = len(obj_list)

        self.total_page = int(self.total / self.size) + 1 \
            if self.total % self.size > 0 else int(self.total / self.size)
        self.data = list(obj_list[(
                                          self.cur_page - 1) * self.size: self.cur_page * self.size])
        return self
