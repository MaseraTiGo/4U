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
from tuoen.abs.service.equipment.equipmentout import EquipmentOutServer

import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Search(StaffAuthorizedApi):
    """查詢设备出库数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'agent_name': CharField(desc = "代理商名称", is_required = False),
        'agent_phone': CharField(desc = "代理商电话", is_required = False),
        'product_type': CharField(desc = "产品类型", is_required = False),
        'product_model': CharField(desc = "产品型号", is_required = False),
        'type': CharField(desc = "出库类型", is_required = False),
        'min_number': CharField(desc = "起始号段", is_required = False),
        'max_number': CharField(desc = "终止号段", is_required = False),
        'add_time': DateField(desc = "添加時間", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户返利数据列表', fmt = DictField(desc = "客户返利数据列表", conf = {
        'id': IntField(desc = "id"),
        'agent_name': CharField(desc = "代理商名称"),
        'agent_phone': CharField(desc = "代理商电话"),
        'product_type': CharField(desc = "产品类型"),
        'product_model': CharField(desc = "产品型号"),
        'min_number': CharField(desc = "起始号段"),
        'max_number': CharField(desc = "终止号段"),
        'quantity': IntField(desc = "入库数量"),
        'price': CharField(desc = "单价"),
        'salesman': CharField(desc = "业务员"),
        'address': CharField(desc = "发货地址"),
        'rate': CharField(desc = "签约费率"),
        'type': CharField(desc = "出库类型(self:自营平台,first:一级代理,second:二级代理)"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "创建时间"),
        'add_time': DateField(desc = "添加时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "设备出库数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if 'min_number' in request.search_info:
            min_number = request.search_info.pop('min_number')
            request.search_info.update({'min_number__lte': min_number})
        if 'max_number' in request.search_info:
            max_number = request.search_info.pop('max_number')
            request.search_info.update({'max_number__gte': max_number})
        page_list = EquipmentOutServer.search(request.current_page, **request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 進行了出庫設備查詢操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "出庫設備查詢"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.LOOK, record_detail, remark)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': equipmentout.id,
            'agent_name': equipmentout.agent_name,
            'agent_phone': equipmentout.agent_phone,
            'product_type': equipmentout.product_type,
            'product_model': equipmentout.product_model,
            'min_number': equipmentout.min_number,
            'max_number': equipmentout.max_number,
            'quantity': equipmentout.quantity,
            'price': equipmentout.price,
            'salesman': equipmentout.salesman,
            'address': equipmentout.address,
            'rate': equipmentout.rate,
            'type': equipmentout.type,
            'remark': equipmentout.remark,
            'create_time': equipmentout.create_time,
            'add_time': equipmentout.add_time,
        } for equipmentout in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Update(StaffAuthorizedApi):
    """入庫設備編輯"""
    request = with_metaclass(RequestFieldSet)
    request.eo_id = RequestField(IntField, desc = '出庫設備id')
    request.eo_info = RequestField(DictField, desc = "設備详情", conf = {
        'agent_name': CharField(desc = "代理商名称", is_required = False),
        'agent_phone': CharField(desc = "代理商電話", is_required = False),
        'product_type': CharField(desc = "产品类型", is_required = False),
        'product_model': CharField(desc = "产品型号", is_required = False),
        'min_number': CharField(desc = "起始号段", is_required = False),
        'max_number': CharField(desc = "终止号段", is_required = False),
        'quantity': CharField(desc = "入库数量", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
        'type': CharField(desc = "出库类型", is_required = False),
        'add_time': DateField(desc = "添加时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改出庫設備接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        EquipmentOutServer.update(request.eo_id, **request.eo_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 對出庫設備條目{id}進行編輯操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = request.eo_id)
        remark = "出庫設備編輯"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.EDIT, record_detail, remark)

    def fill(self, response):
        return response
