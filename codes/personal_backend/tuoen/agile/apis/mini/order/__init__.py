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


class Search(MiniAuthorizedApi):
    """订单信息"""
    request = with_metaclass(RequestFieldSet)
    request.order_sn_list = RequestField(ListField, desc = '订单列表', fmt = CharField(desc = '订单id'))

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '订单列表', fmt = DictField(desc = "订单列表", conf = {
        'order_sn': CharField(desc = "订单编号"),
        'logistics_list': ListField(desc = '物流列表', fmt = DictField(desc = "物流列表", conf = {
           'company': CharField(desc = "物流公司"),
           'number': CharField(desc = "物流单号"),
        })),
        'sn_list': ListField(desc = 'sn号码列表', fmt = CharField(desc = "sn号码列表")),
    }))

    @classmethod
    def get_desc(cls):
        return "订单信息"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        order_qs = OrderServer.search_qs(order_sn__in = request.order_sn_list)
        order_list = LogisticsServer.hung_logistics_fororder(order_qs)
        order_list = EquipmentSnServer.hung_sn_fororder(order_list)

        return order_list

    def fill(self, response, order_list):
        response.data_list = [{
            'order_sn': order.order_sn,
            'logistics_list':[{
                         'company':logistics.company,
                         'number':logistics.number,
                         } for logistics in order.logistics_list],
            'sn_list':[equipment_sn.code for equipment_sn in order.sn_list]
        } for order in order_list]
        return response
