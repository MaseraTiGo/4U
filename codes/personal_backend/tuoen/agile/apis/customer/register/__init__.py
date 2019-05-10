# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField, DateField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.customer.manager import CustomerRegisterServer


class Search(StaffAuthorizedApi):
    """客户註冊列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "客户編碼", is_required = False),
        'device_code': CharField(desc = "设备编码", is_required = False),
        'bind_time_start': DatetimeField(desc = "綁定开始時間", is_required = False),
        'bind_time_end': DatetimeField(desc = "綁定结束時間", is_required = False),
        'status': CharField(desc = "狀態", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户列表', fmt = DictField(desc = "客户列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "姓名"),
        'code': CharField(desc = "客戶編碼"),
        'phone': CharField(desc = "註冊手機號"),
        'agent_name': CharField(desc = "代理商名稱"),
        'device_code': CharField(desc = "设备编码"),
        'register_time': DatetimeField(desc = "註冊時間"),
        'bind_time': DatetimeField(desc = "綁定時間"),
        'status': CharField(desc = "状态"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户註冊列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = CustomerRegisterServer.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
                'id': customer.id,
                'name': customer.name,
                'code': customer.code,
                'agent_name': customer.agent_name,
                'device_code': customer.equipment.code if customer.equipment else customer.device_code,
                'phone': customer.phone,
                'register_time': customer.register_time,
                'bind_time': customer.bind_time,
                'status': customer.status,
        } for customer in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page

        return response
