# coding=UTF-8

from tuoen.sys.core.field.base import CharField, FileField, DictField, IntField, \
                                      ListField, DatetimeField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

from tuoen.agile.apis.server import MiniAuthorizedApi

from tuoen.abs.service.order.manager import OrderServer
from tuoen.abs.service.logistics.manager import LogisticsServer
from tuoen.abs.service.equipment.manager import EquipmentSnServer
from tuoen.abs.service.customer.manager import CustomerRegisterServer
from tuoen.abs.service.customer.transaction import TransactionServer


class Search(MiniAuthorizedApi):
    """客户流水数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.sn_list = RequestField(ListField, desc = 'sn列表', fmt = CharField(desc = 'sn号'))
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'transaction_time_start': DatetimeField(desc = "交易开始时间"),
        'transaction_time_end': DatetimeField(desc = "交易终止时间"),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户流水数据列表', fmt = DictField(desc = "客户流水数据列表", conf = {
            'device_code': CharField(desc = "sn码"),
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


    @classmethod
    def get_desc(cls):
        return "客户流水数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        customer_register_qs = CustomerRegisterServer.search_all(device_code__in = request.sn_list)
        if 'transaction_time_start' in request.search_info:
            transaction_time_start = request.search_info.pop('transaction_time_start')
            request.search_info.update({'transaction_time__gte': transaction_time_start})
        if 'transaction_time_end' in request.search_info:
            transaction_time_end = request.search_info.pop('transaction_time_end')
            request.search_info.update({'transaction_time__lte': transaction_time_end})
        transaction_list = TransactionServer.hung_transaction_forregister(customer_register_qs, **request.search_info)

        return transaction_list

    def fill(self, response, transaction_list):
        response.data_list = [{
                    'device_code': transaction.device_code,
                    'agent_name': transaction.agent_name,
                    'service_code': transaction.service_code,
                    'code': transaction.register_code,
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
        } for transaction in transaction_list]

        return response

