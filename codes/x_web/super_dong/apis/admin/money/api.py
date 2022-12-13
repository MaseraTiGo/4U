# -*- coding: utf-8 -*-
# @File    : api
# @Project : djangoProject
# @Time    : 2022/10/12 11:09
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from super_dong.apis.admin.money.manager import MyShitManager
from super_dong.frame.core.api import AuthApi
from super_dong.frame.core.data_field import CharField, IntField, DateTimeField, \
    AlmightyField, BooleanField
from super_dong.frame.core.data_field.data_type import RequestData


class Create(AuthApi):
    class data(RequestData):
        name = CharField(
            verbose='fucking name', max_length=-1
        )
        amount = IntField(verbose='fucking age')
        invest_type = IntField(
            verbose='invest type',
            choices=MyShitManager.InvestType_Choices
        )
        status = IntField(
            verbose="invest status",
            choices=MyShitManager.Status_Choices
        )
        app = IntField(verbose='app type', choices=MyShitManager.App_Choices)
        ex_info = AlmightyField(verbose='ex info', is_required=False)
        remake = CharField(verbose='actually remark', max_length=128,
                           is_required=False)

    @classmethod
    def get_desc(cls):
        pass

    @classmethod
    def get_author(cls):
        pass

    @classmethod
    def get_history(cls):
        pass

    @classmethod
    def get_unique_num(cls):
        pass

    def execute(self):
        MyShitManager.create(**self.data.as_dict())

    def tidy(self, *ret):
        pass


class QuickCreate(AuthApi):
    class data(RequestData):
        record_datetime = DateTimeField(verbose='fucking name',
                                        is_required=False)
        yesterday_only = BooleanField(
            verbose='use latest data',
            is_required=False,
            default=True
        )

    @classmethod
    def get_desc(cls):
        pass

    @classmethod
    def get_author(cls):
        pass

    @classmethod
    def get_history(cls):
        pass

    @classmethod
    def get_unique_num(cls):
        pass

    def execute(self):
        print(f"dong ------------>: {self.data.as_dict()}")
        MyShitManager.quick_create(**self.data.as_dict())

    def tidy(self, *ret):
        pass
