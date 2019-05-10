# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.customer.rebate import RebateServer


from tuoen.abs.service.authority import UserRightServer

import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Search(StaffAuthorizedApi):
    """返利搜索列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'agent_name': CharField(desc = "代理商名稱", is_required = False),
        'name': CharField(desc = "客戶姓名", is_required = False),
        'phone': CharField(desc = "註冊手機號", is_required = False),
        'code': CharField(desc = "客戶編碼", is_required = False),
        'device_code': CharField(desc = "設備編碼", is_required = False),
        'is_rebate': CharField(desc = "是否返利", is_required = False),
        'month_start_time': DateField(desc = "起始時間", is_required = False),
        'month_end_time': DateField(desc = "終止時間", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='客户返利数据列表', fmt=DictField(desc="客户返利数据列表", conf={
        'id': IntField(desc="id"),
        'agent_id': CharField(desc="代理商ID"),
        'agent_name': CharField(desc="代理商名称"),
        'code': CharField(desc="客户编码"),
        'name': CharField(desc="客户名称"),
        'phone': CharField(desc="注册手机号"),
        'activity_type': CharField(desc="活动类型"),
        'device_code': CharField(desc="设备编码"),
        'register_time': DateField(desc="注册时间"),
        'bind_time': DatetimeField(desc="绑定时间"),
        'month': DateField(desc="交易月份"),
        'transaction_amount': IntField(desc="交易金额/分"),
        'effective_amount': IntField(desc="有效金额/分"),
        'accumulate_amount': IntField(desc="当月累计交易金额/分"),
        'history_amount': IntField(desc="历史累计交易金额/分"),
        'type': CharField(desc="号段类型"),
        'is_rebate': CharField(desc="是否返利"),
        'remark': CharField(desc="备注"),
        'create_time': DatetimeField(desc="创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "返利列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if 'code' in request.search_info:
            code = request.search_info.pop('code')
            request.search_info.update({'code__code': code})
        if 'device_code' in request.search_info:
            device_code = request.search_info.pop('device_code')
            request.search_info.update({'code__device_code': device_code})
        if 'month_start_time' in request.search_info:
            month_start_time = request.search_info.pop('month_start_time')
            request.search_info.update({'month__gte': month_start_time})
        if 'month_end_time' in request.search_info:
            month_end_time = request.search_info.pop('month_end_time')
            request.search_info.update({'month__lte': month_end_time})
        rebate_pages = RebateServer.search(request.current_page, **request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 進行了返利查詢操作".format(who=staff.name,
                                                                      datetime=datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "返利查詢"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.LOOK, record_detail, remark)
        return rebate_pages

    def fill(self, response, page_list):
        response.data_list = [{
            'id': rebate.id,
            'agent_id': rebate.agent_id,
            'agent_name': rebate.agent_name,
            'code': rebate.code.code,
            'name': rebate.name,
            'phone': rebate.phone,
            'activity_type': rebate.activity_type,
            'device_code': rebate.code.device_code,
            'register_time': rebate.register_time,
            'bind_time': rebate.bind_time,
            'month': rebate.month,
            'transaction_amount': rebate.transaction_amount,
            'effective_amount': rebate.effective_amount,
            'accumulate_amount': rebate.accumulate_amount,
            'history_amount': rebate.history_amount,
            'type': rebate.type,
            'is_rebate': rebate.is_rebate,
            'remark': rebate.remark,
            'create_time': rebate.create_time,
        } for rebate in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
