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

from tuoen.abs.service.customer.transaction import TransactionServer

import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Search(StaffAuthorizedApi):
    """客户流水数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "客户编码", is_required = False),
        'agent_name': CharField(desc = "代理商名称", is_required = False),
        'service_code': CharField(desc = "服务编码", is_required = False),
        'type': CharField(desc = "号段类型", is_required = False),
        'transaction_status': CharField(desc = "交易状态", is_required = False),
        'transaction_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'transaction_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户流水数据列表', fmt = DictField(desc = "客户流水数据列表", conf = {
        'id': IntField(desc = "id"),
        'agent_name': CharField(desc = "代理商名称"),
        'service_code': CharField(desc = "服务编码"),
        'code': CharField(desc = "客户编码"),
        'phone': CharField(desc = "手机号"),
        'transaction_time': CharField(desc = "交易时间"),
        'transaction_code': CharField(desc = "流水编号"),
        'transaction_money': IntField(desc = "交易金额"),
        'fee': IntField(desc = "手续费/分"),
        'good_service_fee': IntField(desc = "优享手续费/分"),
        'rate': IntField(desc = "客户费率"),
        'good_service_rate': IntField(desc = "优享费率"),
        'other_fee': IntField(desc = "其他手续费/分"),
        'transaction_status': CharField(desc = "交易状态"),
        'type': CharField(desc = "号段类型"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户流水数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if 'code' in request.search_info:
            code = request.search_info.pop('code')
            request.search_info.update({'code__code': code})
        if 'transaction_time_start' in request.search_info:
            transaction_time_start = request.search_info.pop('transaction_time_start')
            request.search_info.update({'transaction_time__gte': transaction_time_start})
        if 'transaction_time_end' in request.search_info:
            transaction_time_end = request.search_info.pop('transaction_time_end')
            request.search_info.update({'transaction_time__lte': datetime.datetime(transaction_time_end.year, \
                                            transaction_time_end.month, transaction_time_end.day, 23, 59, 59)})
        page_list = TransactionServer.search(request.current_page, **request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 進行了交易流水查詢操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "交易流水查詢"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.LOOK, record_detail, remark)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': transaction.id,
            'agent_name': transaction.agent_name,
            'service_code': transaction.service_code,
            'code': transaction.code.code,
            'phone': transaction.phone,
            'transaction_time': transaction.transaction_time,
            'transaction_code':transaction.transaction_code,
            'transaction_money': transaction.transaction_money,
            'fee': transaction.fee,
            'good_service_fee': transaction.good_service_fee,
            'rate': transaction.rate,
            'good_service_rate': transaction.good_service_rate,
            'other_fee': transaction.other_fee,
            'transaction_status': transaction.transaction_status,
            'type': transaction.type,
            'create_time': transaction.create_time,
        } for transaction in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
