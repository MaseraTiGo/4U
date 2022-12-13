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
