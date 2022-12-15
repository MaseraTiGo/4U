# -*- coding: utf-8 -*-
# @File    : manager
# @Project : djangoProject
# @Time    : 2022/12/9 20:31
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import datetime

from super_dong.frame.core.exception import BusinessLogicError


class BaseManager(object):
    MODEL = None

    # def __init_subclass__(cls, **kwargs):
    #     if cls.MODEL is None:
    #         raise NotImplementedError("MODEL must be defined in your own class")

    @classmethod
    def search(cls, **search_info):
        return cls.MODEL.search(**search_info)

    @classmethod
    def create(cls, **create_info):
        return cls.MODEL.create(**create_info)

    @classmethod
    def search_date(cls, date, col="create_time"):
        if date is None:
            raise BusinessLogicError(f"date can not be none.")
        if isinstance(date, datetime.datetime):
            date = date.date()
        search_info = {
            f"{col}__gte": f"{str(date)} 00:00:00",
            f"{col}__lte": f"{str(date)} 23:59:59"
        }
        return cls.search(**search_info)
