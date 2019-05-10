# coding=UTF-8

# 环境的
import re
# 第三方
import datetime
# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.security import Security
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField, DateField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.service.manager import ServiceServer
from tuoen.abs.service.service.manager import ServiceItemServer
from tuoen.abs.service.order.manager import OrderServer

class Search(StaffAuthorizedApi):
    """设备质检产品列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        "equipment_code":CharField(desc = "设备编码", is_required = False),
        "name":CharField(desc = "购买人姓名", is_required = False),
        "phone":CharField(desc = "购买人手机号", is_required = False),
        "order_sn":CharField(desc = "订单号", is_required = False),
        'shop_name': CharField(desc = "店铺名称", is_required = False),
        # "buy_date_start": DateField(desc="购买起始时间", is_required=False),
        # "buy_date_end": DateField(desc="购买结束时间", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '设备质检产品列表', fmt = DictField(desc = "设备质检产品列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "购买人", reprocess = Security.name_encryption),
        'phone': CharField(desc = "购买人电话", reprocess = Security.mobile_encryption),
        'equipment_status': CharField(desc = "设备状态"),
        'code': CharField(desc = "SN码"),
        'phone_code': CharField(desc = "手机编码"),
        'device_type': CharField(desc = "设备类型"),
        'pre_id': IntField(desc = "售前客服id"),
        'pre_name': CharField(desc = "售前客服"),
        'after_id': IntField(desc = "售后客服id"),
        'after_name': CharField(desc = "售后客服"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'buy_time': DatetimeField(desc = "购买时间"),
        'create_time': DatetimeField(desc = "录入时间"),
        'buyinfo_status': CharField(desc = "购买信息状态"),
        'dsinfo_status': CharField(desc = "电刷信息状态"),
        'rebate_status': CharField(desc = "激活信息状态"),
        'remark': CharField(desc = "訂單備註"),
        'order_sn':CharField(desc = "订单号"),
        'sn_status': CharField(desc = "设备码出入库状态"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "设备质检列表接口"

    @classmethod
    def get_author(cls):
        return "fsy_"

    def execute(self, request):
        if "shop_name" in request.search_info:
            shop_name = request.search_info.pop("shop_name")
            request.search_info.update({'order__shop__name': shop_name})
        if "equipment_code" in request.search_info:
            equipment_code = request.search_info.pop("equipment_code")
            request.search_info.update({"equipment_sn__code": equipment_code})
        if "name" in request.search_info:
            customer_name = request.search_info.pop("name")
            request.search_info.update({"customer__name": customer_name})
        if "order_sn" in request.search_info:
            order_sn = request.search_info.pop("order_sn")
            request.search_info.update({"order__order_sn": order_sn})
        if "phone" in request.search_info:
            customer_phone = request.search_info.pop("phone")
            request.search_info.update({"customer__phone": customer_phone})
        # may be open later,so keep it.
        if "buy_date_start" in request.search_info:
            buy_date_start = request.search_info.pop("buy_date_start")
            request.search_info.update({"order__pay_time__gte": buy_date_start})
        if "buy_date_end" in request.search_info:
            buy_date_end = request.search_info.pop("buy_date_end")
            request.search_info.update({"order__pay_time__lte":\
                                datetime.datetime(buy_date_end.year, buy_date_end.month, buy_date_end.day, 23, 59, 59)})
        if not request.search_info:
            request.search_info.update({'id':-3})
        page_list = ServiceItemServer.search(request.current_page, **request.search_info)
        # 挂载售前售后客服
        ServiceServer.hung_staff_forservice(page_list.data)
        # 挂载手机编码
        ServiceItemServer.hung_phonecode_forservice(page_list.data)
        # 挂载店铺
        OrderServer.hung_shop_forservice(page_list.data)
        # 挂载设备类型
        ServiceItemServer.hung_devicetype_forservice(page_list.data)

        if self.auth_user.is_security:
            self.response.on_safe()

        return page_list

    def hide_str(self, proc_str):
        if re.search("\d+", proc_str):
            proc_str = proc_str[:3] + '****' + proc_str[-4:]
        else:
            proc_str = proc_str[:1] + '*' * (len(proc_str) - 1)
        return proc_str

    def fill(self, response, page_list):
        response.data_list = [{
            'id': service_item.id,
            'name': self.hide_str(service_item.customer.name) if service_item.customer else "",
            'phone': self.hide_str(service_item.customer.phone) if service_item.customer else "",
            'code': service_item.equipment_sn.code,
            'phone_code': service_item.phone_code,
            'equipment_status': service_item.equipment_sn.sn_status,
            'device_type': service_item.device_type,
            'pre_id': service_item.pre_staff.id if service_item.pre_staff else 0,
            'pre_name': service_item.pre_staff.name if service_item.pre_staff else "",
            'after_id': service_item.after_staff.id if service_item.after_staff else 0,
            'after_name': service_item.after_staff.name if service_item.after_staff else "",
            'shop_id': service_item.shop.id if service_item.shop else 0,
            'shop_name': service_item.shop.name if service_item.shop else "",
            'buy_time': service_item.order.pay_time if service_item.order else "",
            'create_time': service_item.create_time,
            'buyinfo_status': service_item.buyinfo_status,
            'dsinfo_status': service_item.dsinfo_status,
            'rebate_status': service_item.rebate_status,
            'order_sn':service_item.order.order_sn if service_item.order else "",
            'remark': service_item.order.remark if service_item.order else "",
            'sn_status': service_item.sn_status,
        } for service_item in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response
