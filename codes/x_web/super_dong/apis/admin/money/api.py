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
from super_dong.frame.core.api_doc import ApiDocGenerator
from super_dong.frame.core.data_field import CharField, IntField, DateTimeField, \
    AlmightyField, BooleanField, DateField, ListField, DictField, FloatField
from super_dong.frame.core.data_field.data_type import RequestData, ResponseData


class Create(AuthApi):
    class data(RequestData):
        """create info"""
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


class Delete(AuthApi):
    class data(RequestData):
        id_ = IntField(verbose="id")

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
        MyShitManager.quick_create(**self.data.id_)

    def tidy(self, *ret):
        pass


class Update(AuthApi):
    class data(RequestData):
        id_ = IntField(verbose="id")
        name = CharField(
            verbose='fucking name', max_length=-1, is_required=False
        )
        amount = FloatField(verbose='fucking age', is_required=False)
        invest_type = IntField(
            verbose='invest type',
            choices=MyShitManager.InvestType_Choices,
            is_required=False
        )
        status = IntField(
            verbose="invest status",
            choices=MyShitManager.Status_Choices,
            is_required=False
        )
        app = IntField(
            verbose='app type',
            choices=MyShitManager.App_Choices,
            is_required=False
        )
        ex_info = AlmightyField(verbose='ex info', is_required=False)
        remark = CharField(
            verbose='actually remark',
            max_length=128,
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
        MyShitManager.update(**self.data.as_dict())

    def tidy(self, *ret):
        pass


class CalNetWorth(AuthApi):
    class data(RequestData):
        date = DateField(verbose='calculate date', is_required=False)

    @classmethod
    def get_desc(cls):
        return "api 4 CalNetWorth"

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
        MyShitManager.calculate_net_worth(self.data.as_dict().get('date'))

    def tidy(self, *ret):
        pass


class ShitProfile(AuthApi):
    class data(ResponseData):
        profile = AlmightyField(verbose='almighty profile')

    @classmethod
    def get_desc(cls):
        return "api 4 ShitProfile"

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
        return MyShitManager.shit_profile()

    def tidy(self, *ret):
        return {
            "data": {
                "profile": ret[0]
            }
        }


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


class SortByApp(AuthApi):
    class req_data(RequestData):
        app = IntField(verbose='app type', choices=MyShitManager.App_Choices, is_required=False)

    class rsp_data(ResponseData):
        data = AlmightyField(verbose='details')

    @classmethod
    def get_desc(cls):
        return "api 4 SortByApp"

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
        return MyShitManager.sort_by_app(self.req_data.as_dict())

    def tidy(self, *ret):
        return {
            'rsp_data': {
                'data': ret[0]
            }
        }
