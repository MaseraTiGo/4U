# coding=UTF-8

# 环境的
from io import StringIO
from django.http import HttpResponse
import json
# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.order.manager import ReplenishmentServer
from tuoen.abs.service.authority import UserRightServer
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware


class Search(StaffAuthorizedApi):
    """补货单列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "设备编码", is_required = False),
        'consignee': CharField(desc = "购买人", is_required = False),
        'order_sn': CharField(desc = "订单号", is_required = False),
        'phone': CharField(desc = "购买人电话", is_required = False),
        'department': IntField(desc = "部门", is_required = False),
        'seller': IntField(desc = "售前客服", is_required = False),
        'shop': CharField(desc = "店铺", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '退貨订单列表', fmt = DictField(desc = "退貨订单列表", conf = {
        'id': IntField(desc = "id"),
        'order_sn': CharField(desc = "订单号"),
        'replenishment_num': CharField(desc = "补货单号"),
        'src_code': CharField(desc = "设备编码"),
        'status': CharField(desc = "补货状态"),
        'seller': CharField(desc = "售前客服"),
        'phone_code': CharField(desc = "手机编码"),
        'goods_name': CharField(desc = "商品名称"),
        'count': IntField(desc = "数量"),
        'amount': CharField(desc = "订单金额"),
        'shop': CharField(desc = "购买店铺"),
        'customer': CharField(desc = "购买人"),
        'phone_num': CharField(desc = "购买电话"),
        'shipping_address': CharField(desc = "收货地址"),
        'buy_time': DatetimeField(desc = "购买时间"),
        'create_time': DatetimeField(desc = "添加时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "补货单列表接口"

    @classmethod
    def get_author(cls):
        return "fsy_d"

    def execute(self, request):
        # add search action
        user = self.auth_user
        user = UserRightServer(user)
        request.search_info.update({'staff__id__in': user._staff_id_list})
        page_list = ReplenishmentServer.search(request.current_page, **request.search_info)
        # hung all info that's needed
        ReplenishmentServer.hung_all(page_list.data)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 进行了退货订单查询操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "退货订单查询"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff,
                                   OperationTypes.STAFF, JournalTypes.SEARCH, record_detail, remark)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': ri.id,
            'replenishment_num': ri.replenishment.replenishment_num if ri.replenishment else '',
            'order_sn': ri.replenishment.order.order_sn if ri.replenishment.order else '',
            'src_code': ri.code.code if ri.code else '',
            'status': ri.status,
            'amount': ri.amount,
            'count': ri.replenishment.quantity,
            'shipping_address': ri.replenishment.order.address if ri.replenishment.order else '',
            'customer': ri.replenishment.order.consignee if ri.replenishment.order else '',
            'phone_num': ri.replenishment.order.phone if ri.replenishment.order else '',
            'department': ri.department,
            'seller': ri.seller,
            'phone_code': ri.replenishment.order.customer.mobiledevices.code if ri.replenishment.order.customer.mobiledevices else '',
            'goods_name': ri.goods.name if ri.goods else '',
            'shop': ri.replenishment.order.shop.name if ri.replenishment.order.shop else '',
            'remark': ri.remark,
            'buy_time': ri.replenishment.order.pay_time if ri.replenishment.order else '',
            'create_time': ri.create_time,
            } for ri in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Remove(StaffAuthorizedApi):
    """刪除补货訂單"""
    request = with_metaclass(RequestFieldSet)
    request.replenishment_item_id = RequestField(IntField, desc = "补货单详情id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "补货單删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        replenishment_item = ReplenishmentServer.get(request.replenishment_item_id)
        ReplenishmentServer.remove(replenishment_item)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对SN为{code}进行了补货单删除操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = replenishment_item.code.code)
        remark = "补货单删除操作"
        JournalMiddleware.register(staff, "staff", staff,
                                    "staff", "remove", record_detail, remark)
    def fill(self, response):
        return response


class Export(StaffAuthorizedApi):
    """导出补货单"""
    request = with_metaclass(RequestFieldSet)
    request.ri_id = RequestField(CharField, desc = "需要导出的ID列表")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "设备编码", is_required = False),
        'consignee': CharField(desc = "购买人", is_required = False),
        'order_sn': CharField(desc = "订单号", is_required = False),
        'phone': CharField(desc = "购买人电话", is_required = False),
        'department': CharField(desc = "部门", is_required = False),
        'seller': CharField(desc = "售前客服", is_required = False),
        'shop': CharField(desc = "店铺", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })
    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = "导出数据列表", fmt = DictField(desc = "详细信息", conf = {
        'order_sn': CharField(desc = "网店订单编号"),
        'goods_name': CharField(desc = "商品名称"),
        'goods_num': CharField(desc = "商品编码"),
        'order_status': CharField(desc = "订单状态"),
        'quantity': CharField(desc = "数量"),
        'price': CharField(desc = "单价"),
        'pay_time': CharField(desc = "订单日期"),
        'consignee': CharField(desc = "收货人名称"),
        'telephone': CharField(desc = "收货人电话"),
        'cell_phone': CharField(desc = "收货人手机"),
        'province': CharField(desc = "省份"),
        'city': CharField(desc = "市"),
        'area': CharField(desc = "区"),
        'address': CharField(desc = "收货地址"),
        'buyer_account': CharField(desc = "买家帐号"),
        'delivery': CharField(desc = "物流公司"),
        'delivery_num': CharField(desc = "物流单号"),
        'buyer_fee': CharField(desc = "买家运费"),
        'buyer_message': CharField(desc = "买家留言"),
        'seller_remark': CharField(desc = "卖家备注"),
        'invoice': CharField(desc = "发票抬头"),
        'order_remark': CharField(desc = "订单备注"),
    }))

    @classmethod
    def get_desc(cls):
        return "补货單导出接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        ri_id = json.loads(request.ri_id)
        result_list = ReplenishmentServer.export(ri_id, **request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对补货单进行了导出操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "补货单导出操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff,
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
        return result_list

    def fill(self, response, result_list):
        response.data_list = [{
            'order_sn': item['order_sn'],
            'goods_name': item['goods_name'],
            'goods_num': item['goods_num'],
            'order_status': item['order_status'],
            'quantity': item['quantity'],
            'price': item['price'],
            'pay_time': item['pay_time'],
            'consignee': item['consignee'],
            'telephone': item['telephone'],
            'cell_phone': item['cell_phone'],
            'province': item['province'],
            'city': item['city'],
            'area': item['area'],
            'address': item['address'],
            'buyer_account': item['buyer_account'],
            'delivery': item['delivery'],
            'delivery_num': item['delivery_num'],
            'buyer_fee': item['buyer_fee'],
            'buyer_message': item['buyer_message'],
            'seller_remark': item['seller_remark'],
            'invoice': item['invoice'],
            'order_remark': item['order_remark']
        } for item in result_list]
        return response
