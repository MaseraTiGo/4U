# -*- coding: utf-8 -*-
# @File    : api
# @Project : x_web
# @Time    : 2023/1/9 9:21
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from datetime import datetime

from super_dong.frame.core.api import AuthApi
from super_dong.frame.core.api_doc import ApiDocGenerator
from super_dong.frame.core.data_field import CharField, IntField, DateTimeField, \
    ListField, DictField, FuzzyDictField
from super_dong.frame.core.data_field.data_type import RequestData, ResponseData


class DocTest(AuthApi):
    class req_data(RequestData):
        """this is just a request data lalala"""

        data = ListField(
            verbose='list test',
            item=DictField(
                verbose='item detail',
                members={
                    'id': IntField(verbose='id'),
                    'name': CharField(verbose='name'),
                    "hobbit": ListField(
                        verbose="hobbits",
                        item=DictField(
                            verbose="dict",
                            members={
                                "name": CharField(verbose="hobbit name"),
                                "date": DateTimeField(verbose="love date")
                            }
                        )
                    )
                }, strict=True)
        )

        fuck = ListField(verbose='test test',
                         item=CharField(verbose='fuck you'), is_required=False)

    class req_data2(RequestData):
        """this is just a request data lalala"""

        data = ListField(
            verbose='list test',
            item=DictField(
                verbose='item detail',
                members={
                    'id': IntField(verbose='id'),
                    'name': CharField(verbose='name', is_required=False,
                                      choices=[("apple", "APPLE")],
                                      default="apple"),
                    "hobbit": ListField(
                        verbose="hobbits",
                        item=DictField(
                            verbose="dict",
                            members={
                                "name": CharField(verbose="hobbit name"),
                                "date": DateTimeField(verbose="love date")
                            }
                        )
                    )
                }, strict=True)
        )

        fuck = ListField(verbose='test test',
                         item=CharField(verbose='fuck you'), is_required=False)

    @classmethod
    def get_desc(cls):
        return "api 4 DocTest"

    @classmethod
    def get_author(cls):
        return "superDong"

    @classmethod
    def get_history(cls):
        return "Alpha-001"

    @classmethod
    def get_unique_num(cls):
        return 100001

    def execute(self):
        ApiDocGenerator.the_doke()
        pass

    def tidy(self, *ret):
        pass


class TestFuzzyDict(AuthApi):
    class req_data(RequestData):
        fuck = FuzzyDictField(
            verbose="fuzzy dict",
            key_field=CharField(verbose='key'),
            value_field=CharField(verbose='value')
        )

    class rsp_data(ResponseData):
        damn = FuzzyDictField(
            verbose="fuzzy dict",
            key_field=CharField(verbose='key'),
            value_field=ListField(
                verbose='value',
                item=IntField(
                    verbose='int',
                    max_value=100
                )
            )
        )

    @classmethod
    def get_desc(cls):
        return "api 4 TestFuzzyDict"

    @classmethod
    def get_author(cls):
        return "superDong"

    @classmethod
    def get_history(cls):
        return "Alpha-001"

    @classmethod
    def get_unique_num(cls):
        return 100001

    def execute(self):
        return {
            "apple": [1, 2, 3],
            "banana": [4, 5, 600]
        }

    def tidy(self, *ret):
        return {
            "rsp_data": {
                "damn": ret[0]
            }
        }


class TestNoArgs(AuthApi):
    # class req_data(RequestData):
    #     pass

    class rsp_data(ResponseData):
        data = CharField(verbose='test', default='fucking test',
                         is_required=False)

    @classmethod
    def get_desc(cls):
        return "api 4 TestNoArgs"

    @classmethod
    def get_author(cls):
        return "superDong"

    @classmethod
    def get_history(cls):
        return "Alpha-001"

    @classmethod
    def get_unique_num(cls):
        return 100001

    def execute(self):
        return "fuck"

    def tidy(self, *ret):
        return {
            "rsp_data": {
                # "data": ret[0]
            }
        }


class TestToStr(AuthApi):
    # class req_data(RequestData):
    #     pass

    class rsp_data(ResponseData):
        day = DateTimeField(
            verbose='datetime',
            is_required=False,
        )

    @classmethod
    def get_desc(cls):
        return "api 4 ToStr"

    @classmethod
    def get_author(cls):
        return "superDong"

    @classmethod
    def get_history(cls):
        return "Alpha-001"

    @classmethod
    def get_unique_num(cls):
        return 100001

    def execute(self):
        return datetime.now()

    def tidy(self, *ret):
        return {
            "rsp_data": {
                "day": ret[0]
            }

        }
