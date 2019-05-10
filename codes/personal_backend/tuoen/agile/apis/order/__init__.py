# coding=UTF-8

# 环境的
import json
import datetime
# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.security import Security
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.abs.middleware.department import department_middleware
from tuoen.abs.middleware.journal import JournalMiddleware

from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.order.manager import StaffOrderEventServer, OrderServer, OrderItemServer
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.logistics.manager import LogisticsServer
from tuoen.abs.service.service.manager import ServiceServer
from tuoen.abs.service.equipment.manager import EquipmentServer
from tuoen.abs.service.authority import UserRightServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.order.manager import ReplenishmentServer


class Search(StaffAuthorizedApi):
    """订单列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'order_sn': CharField(desc = "订单号", is_required = False),
        'department': IntField(desc = "部门", is_required = False),
        'server': IntField(desc = "客服", is_required = False),
        'begin_time': DatetimeField(desc="购买起始时间", is_required=False),
        'end_time': DatetimeField(desc="购买终止时间", is_required=False),
        'status': CharField(desc = "订单状态(unpaid:未支付,submit:已下单,payed:已支付,sended:已发货,finished:已完成)", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '订单列表', fmt = DictField(desc = "订单列表", conf = {
        'id': IntField(desc = "id"),
        'order_sn': CharField(desc = "订单编号"),
        'shop_name': CharField(desc = "店铺名称"),
        'consignee': CharField(desc = "收货人"),
        'nick_name': CharField(desc = "昵称"),
        'status': CharField(desc = "订单状态"),
        'pay_time': DatetimeField(desc = "购买时间"),
        'staff_name': CharField(desc = "员工姓名"),
        'staff_id': CharField(desc = "员工id"),
        'department_name': CharField(desc = "部门名称"),
        'department_id': CharField(desc = "部门id"),
        'order_items': ListField(desc = '订单详情', fmt = DictField(desc = "订单详情", conf = {
           'name': CharField(desc = "商品名称"),
           'thumbnail': CharField(desc = "商品缩略图"),
           'rate':CharField(desc = "商品费率"),
           'quantity':IntField(desc = "商品数量"),
           'type':CharField(desc = "商品分类"),
           'brand_name':CharField(desc = "商品型号"),
        })),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "订单列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        user_pro = UserRightServer(staff)
        request.search_info['cur_user'] = user_pro
        if user_pro._is_admin == 1:
            page_list = OrderServer.search(request.current_page, **request.search_info)
        else:
            staff_list = StaffPermiseServer.get_all_children_staff(staff)
            staff_list.append(staff)
            page_list = ServiceServer.search(request.current_page, seller__in = staff_list, cur_user = user_pro)
            order_list = OrderServer.get_order_byservice(page_list.data)
            page_list.data = order_list
        if not user_pro._is_admin:
            department_ids = StaffPermiseServer.get_staff_department_ids(staff)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            page_list.data = list(filter(lambda x: x.id in order_ids, page_list.data))
        page_list.data = StaffOrderEventServer.hung_staff_fororders(page_list.data)
        page_list.data = OrderItemServer.hung_item_fororders(page_list.data)

        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': order.id,
            'order_sn': order.order_sn,
            'shop_name': order.shop.name,
            'consignee': order.consignee,
            'nick_name': order.customer.nick,
            'status': order.status,
            'pay_time': order.pay_time,
            'staff_name': order.staff.name if order.staff else "",
            'staff_id': order.staff.id if order.staff else 0,
            'department_name': order.department.name if order.department else "",
            'department_id': order.department.id if order.department else 0,
            'order_items':[{
                         'name':order_item.name,
                         'thumbnail':order_item.thumbnail,
                         'rate':order_item.rate,
                         'quantity':order_item.quantity,
                         'type':order_item.type,
                         'brand_name':order_item.goods.product_model.name if order_item.goods and order_item.goods.product_model else "",
                         } for order_item in order.items]
        } for order in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取订单详情"""
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = '订单id')

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(DictField, desc = "订单详情", conf = {
        'id': IntField(desc = "id"),
        'order_sn': CharField(desc = "订单编号"),
        'consignee': CharField(desc = "收货人", reprocess = Security.name_encryption),
        'nick_name': CharField(desc = "昵称"),
        'phone': CharField(desc = "收货人电话", reprocess = Security.mobile_encryption),
        'city': CharField(desc = "城市"),
        'address': CharField(desc = "详细地址"),
        'messages': CharField(desc = "买家留言"),
        'paytype': CharField(desc = "支付类型"),
        'pay_time': CharField(desc = "付款时间"),
        'transaction_id': CharField(desc = "第三方支付id"),
        'total_price': IntField(desc = "订单金额"),
        'channel_name': CharField(desc = "渠道名称"),
        'shop_name': CharField(desc = "店铺名称"),
        'create_time': CharField(desc = "创建时间"),
        'remark': CharField(desc = "卖家备注"),
        'returns_items': ListField(desc = '订单详情', fmt = DictField(desc = "订单详情", conf = {
            'returns_num': CharField(desc = "退货单号"),
            're_create_time': DatetimeField(desc = "退货时间"),
            'amount': CharField(desc = "退款金额"),
            're_status': CharField(desc = "退货状态"),
            'product': CharField(desc = "产品"),
            'sn': CharField(desc = "设备编码"),
            'quantity': IntField(desc = "数量"),
            're_remark': IntField(desc = "退货备注"),
        })),
        'replenishment_items': ListField(desc='补货单详情', fmt=DictField(desc="补货单详情", conf={
            'rep_num': CharField(desc="补货单号"),
            'rep_create_time': DatetimeField(desc="补货时间"),
            'rep_status': CharField(desc="退货状态"),
            'rep_product': CharField(desc="产品"),
            'rep_sn': CharField(desc="设备编码"),
            'rep_quantity': IntField(desc="数量"),
            'rep_remark': CharField(desc="备注"),
        })),
        'order_items': ListField(desc = '订单详情', fmt = DictField(desc = "订单详情", conf = {
                'id': IntField(desc = "商品ID"),
               'name': CharField(desc = "商品名称"),
               'sn_list': ListField(desc = "设备编码列表", fmt = DictField(desc = "设备编码列表", conf = {
                    'code': CharField(desc = "设备编码"),
                })),
               'thumbnail': CharField(desc = "商品缩略图"),
               'rate':CharField(desc = "商品费率"),
               'price':IntField(desc = "商品单价"),
               'type':CharField(desc = "商品类型"),
               'brand_name':CharField(desc = "商品型号"),
               'quantity':IntField(desc = "商品数量"),
        })),
        'logistics': ListField(desc = '物流列表', fmt = DictField(desc = "物流列表", conf = {
           'company': CharField(desc = "物流公司"),
           'number': CharField(desc = "物流单号"),
           'total_quantity':IntField(desc = "发货数量"),
           'create_time':DatetimeField(desc = "发货时间"),
           'logistics_items': ListField(desc = "订单详情", fmt = DictField(desc = "订单详情", conf = {
               'name': CharField(desc = "商品名称"),
               'thumbnail': CharField(desc = "商品缩略图"),
               'quantity':IntField(desc = "商品数量"),
               'equipment_codes':ListField(desc = "设备编码列表", fmt = DictField(desc = "设备编码列表", conf = {
                    'code': CharField(desc = "设备编码"),
                })),
            })),
        })),
    })

    @classmethod
    def get_desc(cls):
        return "订单详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        OrderItemServer.hung_item_fororder(order)
        LogisticsServer.hung_item_fororder(order)

        OrderServer.hung_order_returns(order)
        OrderServer.hung_order_replenishment(order)
        if self.auth_user.is_security:
            self.response.on_safe()

        return order

    def fill(self, response, order):
        response.order_info = {
            'id': order.id,
            'order_sn': order.order_sn,
            'consignee': order.consignee,
            'nick_name': order.customer.nick,
            'phone': order.phone,
            'city': order.city,
            'address': order.address,
            'messages': order.messages,
            'paytype': order.paytype,
            'pay_time': order.pay_time,
            'transaction_id': order.transaction_id,
            'total_price': order.total_price,
            'channel_name': order.shop.channel.name if order.shop.channel else "",
            'shop_name': order.shop.name,
            'create_time': order.create_time,
            'remark': order.remark,
            'returns_items': [{
                            'returns_num': item.returns_num,
                            're_create_time': item.create_time,
                            'amount': item.amount,
                            're_status': item.status,
                            'product': item.product,
                            'sn': item.code,

                            'quantity': item.quantity,
                            're_remark': item.remark,
                            } for item in order.returns],
            'replenishment_items': [{
                            'rep_num': item.rep_num,
                            'rep_create_time': item.rep_create_time,
                            'rep_status': item.rep_status,
                            'rep_product': item.rep_product,
                            'rep_sn': item.rep_sn,
                            'rep_quantity': item.rep_quantity,
                            'rep_remark': item.remark,
                            } for item in order.replenishment],
            'order_items':[{
                        'id': orderitem.id,
                        'sn_list': [{
                                 'code': val,
                                 } for val in orderitem.sn_list],
                         'name':orderitem.name,
                         'thumbnail':orderitem.thumbnail,
                         'rate':orderitem.rate,
                         'price':orderitem.price,
                         'type':orderitem.type,
                         'brand_name':orderitem.goods.product_model.name if orderitem.goods and orderitem.goods.product_model else "",
                         'quantity':orderitem.quantity,
                         } for orderitem in order.items],
            'logistics':[{
                         'company': logistics.company,
                         'number': logistics.number,
                         'total_quantity':logistics.total_quantity,
                         'create_time':logistics.create_time,
                         'logistics_items':[{
                             'name': logisticsitem.order_item.name,
                             'thumbnail': logisticsitem.order_item.thumbnail,
                             'quantity':logisticsitem.quantity,
                             'equipment_codes':[{
                                 'code': val,
                                 } for i, val in enumerate(json.loads(logisticsitem.equipment_sn_list))]
                             } for logisticsitem in logistics.items]
                         } for logistics in order.logistics]
        }
        return response


class Transfer(StaffAuthorizedApi):
    """转移订单"""
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = '需要转移的订单id')
    request.staff_id = RequestField(IntField, desc = '转移到的员工id')
    request.department_id = RequestField(IntField, desc = '转移到的部门id')

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "转移订单接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        order = OrderServer.get(request.order_id)
        staff = StaffServer.get(request.staff_id)
        department = department_middleware.get_self(request.department_id)
        OrderServer.transfer_order_tostaff(order, staff, self.auth_user, department)

    def fill(self, response):
        return response

class ApplyForReplenishment(StaffAuthorizedApi):
    """添加补货單"""
    request = with_metaclass(RequestFieldSet)
    request.order_sn = RequestField(CharField, desc = "订单编号")
    request.orderitem_id = RequestField(CharField, desc = "商品详情id")
    request.code_list = RequestField(ListField, desc = "补货前设备SN码", fmt = CharField(desc = "补货前设备SN码"))

    response = with_metaclass(ResponseFieldSet)
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "申请补货单接口"

    @classmethod
    def get_author(cls):
        return "fsy_D"

    def execute(self, request):
        order_item = OrderItemServer.get(request.orderitem_id)
        error_list = ReplenishmentServer.apply_for(request.order_sn, order_item, request.code_list)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对订单{order_sn}下得{info}申请了补货".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), order_sn = request.order_sn,
                                                                      info = request.code_list)
        remark = "申请补货操作"
        JournalMiddleware.register(staff, "staff", staff,
                                   "staff", "add", record_detail, remark)

        return error_list

    def fill(self, response , error_list):
        response.error_list = error_list
        return response
