# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.track.manager import TrackEventServer
from tuoen.abs.service.customer.manager import CustomerServer, SaleChanceServer


class Add(StaffAuthorizedApi):
    """添加跟踪记录"""
    request = with_metaclass(RequestFieldSet)
    request.track_event_info = RequestField(DictField, desc = "跟踪记录", conf = {
        'customer_id': CharField(desc = "客户id"),
        'remark': CharField(desc = "备注说明"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "跟踪记录添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        customer = CustomerServer.get(request.track_event_info['customer_id'])
        request.track_event_info.update({'staff':staff, 'customer':customer})
        TrackEventServer.generate(**request.track_event_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """跟踪列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'customer_id': IntField(desc = "客户id", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '跟踪列表', fmt = DictField(desc = "跟踪列表", conf = {
        'id': IntField(desc = "id"),
        'staff_id': IntField(desc = "客服id"),
        'staff_name': CharField(desc = "客服姓名"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "记录时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "跟踪列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = TrackEventServer.search(request.current_page, **request.search_info)

        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
              'id': track_event.id,
              'staff_id': track_event.staff.id,
              'staff_name': track_event.staff.name,
              'remark': track_event.remark,
              'create_time': track_event.create_time,
        } for track_event in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page

        return response


class SearchByTrack(StaffAuthorizedApi):
    """根据销售机会查询跟踪列表"""
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_id = RequestField(IntField, desc = "销售机会id")

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '跟踪列表', fmt = DictField(desc = "跟踪列表", conf = {
        'id': IntField(desc = "id"),
        'staff_id': IntField(desc = "客服id"),
        'staff_name': CharField(desc = "客服姓名"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "记录时间"),
    }))


    @classmethod
    def get_desc(cls):
        return "根据销售机会查询跟踪列表"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        sale_chance = SaleChanceServer.get(request.sale_chance_id)
        track_list = TrackEventServer.search_by_sale_chance(sale_chance)
        return track_list

    def fill(self, response, track_list):
        response.data_list = [{
              'id': track_event.id,
              'staff_id': track_event.staff.id,
              'staff_name': track_event.staff.name,
              'remark': track_event.remark,
              'create_time': track_event.create_time,
        } for track_event in track_list]

        return response

