# coding=UTF-8

import json
import datetime
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_buyinfo_middleware

from tuoen.abs.middleware.journal import JournalMiddleware
from model.store.model_journal import JournalTypes, OperationTypes

class Upload(StaffAuthorizedApi):
    """客户购买数据导入接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "客户购买数据导入接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_buyinfo_middleware.import_buyinfo(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """客户购买数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'order_sn': CharField(desc = "订单编号", is_required = False),
        'goods_sn': CharField(desc = "商品编号", is_required = False),
        'device_code': CharField(desc = "设备编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户购买数据列表', fmt = DictField(desc = "客户购买数据列表", conf = {
        'id': IntField(desc = "id"),
        'serial_number': IntField(desc = "序号"),
        'order_sn': CharField(desc = "订单编号"),
        'goods_sn': CharField(desc = "商品编号"),
        'buy_number': IntField(desc = "购买数量"),
        'buy_money': IntField(desc = "订单金额/分"),
        'pay_time': DatetimeField(desc = "付款时间"),
        'shop_name': CharField(desc = "网点名称"),
        'buy_name': CharField(desc = "买家姓名"),
        'province': CharField(desc = "省"),
        'city': CharField(desc = "市"),
        'area': CharField(desc = "区"),
        'address': CharField(desc = "详细地址"),
        'logistics_company': CharField(desc = "物流公司"),
        'logistics_code': CharField(desc = "物流单号"),
        'buy_phone': CharField(desc = "联系方式"),
        'status': CharField(desc = "状态"),
        'remark': CharField(desc = "客服备注"),
        'buy_nick': CharField(desc = "卖家账号"),
        'device_code': CharField(desc = "设备编码"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.is_converting = ResponseField(BooleanField, desc = "是否正在转化")

    @classmethod
    def get_desc(cls):
        return "客户购买数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_buyinfo_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': buyinfo.id,
            'serial_number': buyinfo.serial_number,
            'order_sn': buyinfo.order_sn,
            'goods_sn': buyinfo.goods_sn,
            'buy_number': buyinfo.buy_number,
            'buy_money': buyinfo.buy_money,
            'pay_time': buyinfo.pay_time,
            'shop_name': buyinfo.shop_name,
            'buy_name': buyinfo.buy_name,
            'province': buyinfo.province,
            'city': buyinfo.city,
            'area': buyinfo.area,
            'address': buyinfo.address,
            'logistics_company': buyinfo.logistics_company,
            'logistics_code': buyinfo.logistics_code,
            'buy_phone': buyinfo.buy_phone,
            'status': buyinfo.status,
            'remark': buyinfo.remark,
            'buy_nick': buyinfo.buy_nick,
            'device_code': buyinfo.device_code,
            'create_time':buyinfo.create_time,
            'error_text':buyinfo.error_text,
        } for buyinfo in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """客户购买数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户购买数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_buyinfo_middleware.exec_buyinfo(**request.search_info)

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    """客户购买数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.buyinfo_id = RequestField(IntField, desc = '购买信息id')
    request.buyinfo_info = RequestField(DictField, desc = "购买详情", conf = {
        'order_sn': CharField(desc = "订单编号"),
        'goods_sn': CharField(desc = "商品编号"),
        'buy_number': IntField(desc = "购买数量"),
        'buy_money': IntField(desc = "订单金额/分"),
        'pay_time': DatetimeField(desc = "付款时间"),
        'shop_name': CharField(desc = "网点名称"),
        'buy_name': CharField(desc = "买家姓名"),
        'province': CharField(desc = "省"),
        'city': CharField(desc = "市"),
        'area': CharField(desc = "区", is_required = False),
        'address': CharField(desc = "详细地址"),
        'logistics_company': CharField(desc = "物流公司"),
        'logistics_code': CharField(desc = "物流单号"),
        'buy_phone': CharField(desc = "联系方式"),
        'buy_nick': CharField(desc = "卖家账号"),
        'remark': CharField(desc = "客服备注", is_required = False),
        'device_code': CharField(desc = "设备编码", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户购买数据修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       import_buyinfo_middleware.update(request.buyinfo_id, **request.buyinfo_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """購買訂單数据狀態转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '购买信息id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'order_sn': CharField(desc = "订单编号", is_required = False),
        'goods_sn': CharField(desc = "商品编号", is_required = False),
        'device_code': CharField(desc = "设备编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })
    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "購買訂單狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        staff = self.auth_user
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_buyinfo_middleware.reset_status(**request.search_info)
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入购买订单状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response

class Remove(StaffAuthorizedApi):
    """客户购买数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.buyinfo_id = RequestField(CharField, desc = '购买信息id列表')

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户购买数据刪除接口"

    @classmethod
    def get_author(cls):
        return "fsy_"

    def execute(self, request):
        staff = self.auth_user
        buyinfo_list = json.loads(request.buyinfo_id)
        import_buyinfo_middleware.remove(buyinfo_list)
        record_detail = "{who} 在 {datetime} 删除了订单{id}".format(who = staff.name,
                                                                           datetime = datetime.datetime.now().strftime(
                                                                               "%Y-%m-%d %H:%M:%S"), id = buyinfo_list)
        remark = "导入购买订单删除"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.DELETE, record_detail, remark)
    def fill(self, response):
        return response
