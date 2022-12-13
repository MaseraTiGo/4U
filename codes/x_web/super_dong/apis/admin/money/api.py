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
    AlmightyField, BooleanField, DateField, ListField, DictField, FloatField
from super_dong.frame.core.data_field.data_type import RequestData, ResponseData


class Create(AuthApi):
    class data(RequestData):
        name = CharField(
            verbose='fucking name', max_length=-1
        )
        amount = FloatField(verbose='fucking age')
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
        remark = CharField(verbose='actually remark', max_length=128,
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


class Details(AuthApi):
    class search_info(RequestData):
        date = DateField(verbose='fucking date', is_required=False)

    class page_info(RequestData):
        page_num = IntField(verbose='page num', is_required=False, default=1)
        page_size = IntField(verbose='page size', is_required=False, default=10)

    class total(ResponseData):
        total = FloatField(verbose='total shit')

    class data(ResponseData):
        data = ListField(
            verbose='data list',
            item=DictField(verbose='item detail', members={
                'id': IntField(verbose='id'),
                'name': CharField(verbose='name'),
                'amount': FloatField(verbose='amount'),
                'invest_type': CharField(verbose='invest type'),
                'net_worth': FloatField(verbose='net worth'),
                'status': CharField(verbose='status'),
                'app': CharField(verbose='app'),
                'ex_info': AlmightyField(verbose='ex_info'),
                'remark': CharField(verbose='remark'),
                'create_time': DateTimeField(
                    verbose='create time', to_str=True),
            }, strict=True))

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
        return MyShitManager.details(
            self.search_info.as_dict(),
            self.page_info.as_dict()
        )

    def tidy(self, *ret):
        data, total = ret
        return {
            'total': {'total': total},
            'data': {'data': data},
        }
