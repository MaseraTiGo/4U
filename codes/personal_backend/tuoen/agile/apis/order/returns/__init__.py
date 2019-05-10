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
from tuoen.abs.service.order.manager import StaffOrderEventServer, OrderServer, OrderItemServer, OrderReturnsServer
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.logistics.manager import LogisticsServer
from tuoen.abs.service.service.manager import ServiceServer
from tuoen.abs.service.equipment.manager import EquipmentServer
from tuoen.abs.service.authority import UserRightServer
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Search(StaffAuthorizedApi):
    """退貨订单列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "設備編碼", is_required = False),
        'returns_num': CharField(desc = "退货单号", is_required = False),
        'consignee': CharField(desc = "购买人", is_required = False),
        'order_sn': CharField(desc = "订单号", is_required = False),
        'phone': CharField(desc = "电话", is_required = False),
        'department': IntField(desc = "部门", is_required = False),
        'seller': IntField(desc = "售前客服", is_required = False),
        'shop': CharField(desc = "店铺", is_required = False),
        'remark': CharField(desc = "客服备注", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '退貨订单列表', fmt = DictField(desc = "退貨订单列表", conf = {
        'id': IntField(desc = "id"),
        'order_id': IntField(desc = "订单id"),
        'returns_num': CharField(desc = "退货单号"),
        'order_sn': CharField(desc = "订单编号"),
        'code': CharField(desc = "设备编码"),
        'consignee': CharField(desc = "收货人"),
        'phone': CharField(desc = "电话"),
        'department': CharField(desc = "部门"),
        'seller': CharField(desc = "售前客服"),
        'phone_code': CharField(desc = "手机编码"),
        'shop': CharField(desc = "店铺"),
        'remark': CharField(desc = "客服备注"),
        'pay_time': DatetimeField(desc = "添加时间"),
        'create_time': DatetimeField(desc = "添加时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "退貨订单列表接口"

    @classmethod
    def get_author(cls):
        return "fsy_d"

    def execute(self, request):
        staff = self.auth_user
        user_pro = UserRightServer(staff)
        request.search_info['cur_user'] = user_pro
        page_list = OrderReturnsServer.search(request.current_page, **request.search_info)
        # hung department and seller
        OrderReturnsServer.hung_department_seller(page_list.data)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 进行了退货订单查询操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "退货订单查询"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.SEARCH, record_detail, remark)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': ors.id,
            'returns_num': ors.returns_num,
            'order_id': ors.order.id if ors.order else '',
            'order_sn': ors.order.order_sn if ors.order else '',
            'code': ors.code,
            'consignee': ors.order.consignee if ors.order else '',
            'phone': ors.order.phone if ors.order else '',
            'department': ors.department,
            'seller': ors.seller,
            'phone_code': ors.phone_code,
            'shop': ors.order.shop.name if ors.order.shop else '',
            'remark': ors.order.remark if ors.order else '',
            'pay_time': ors.order.pay_time if ors.order else '',
            'create_time': ors.create_time,
            } for ors in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取退貨订单详情"""
    request = with_metaclass(RequestFieldSet)
    request.order_id = RequestField(IntField, desc = '订单id')

    response = with_metaclass(ResponseFieldSet)
    response.order_info = ResponseField(ListField, desc = "订单详情", fmt = DictField(desc = "退貨订单详情列表", conf = {
        'id': IntField(desc = "id"),
        'returns_num': CharField(desc = "退货单号"),
        'create_time': DatetimeField(desc = "退货时间"),
        'amount': CharField(desc = "退款金额"),
        'status': CharField(desc = "退货状态"),
        'product': CharField(desc = "产品"),
        'sn': CharField(desc = "设备编码"),
        'quantity': IntField(desc = "数量"),
    }))

    @classmethod
    def get_desc(cls):
        return "退貨訂單订单详情接口"

    @classmethod
    def get_author(cls):
        return "fsy_d"

    def execute(self, request):
        ors_qs = OrderReturnsServer.get(request.order_id)
        OrderReturnsServer.hung_amount_product(ors_qs)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 查看了退货单为{id}的详情".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "获取退货单详情"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
        return ors_qs

    def fill(self, response, ors_qs):
        response.order_info = [{
            'id': returns.id,
            'returns_num': returns.returns_num,
            'create_time': returns.create_time,
            'amount': returns.amount,
            'status': returns.status,
            'product': returns.product,
            'sn': returns.code,
            'quantity': returns.quantity,
        } for returns in ors_qs]
        return response

class Add(StaffAuthorizedApi):
    """添加退貨訂單"""
    request = with_metaclass(RequestFieldSet)
    request.returns_info = RequestField(DictField, desc = "退貨訂單详情", conf = {
        'code': CharField(desc = "設備編碼"),
        'remark': CharField(desc = "訂單編號", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加退貨訂單接口"

    @classmethod
    def get_author(cls):
        return "fsy_"

    def execute(self, request):
        code = request.returns_info['code']
        OrderReturnsServer.add(**request.returns_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对SN号为:{code}进行了退货".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = code)
        remark = "退货操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.ADD, record_detail, remark)
    def fill(self, response):
        return response

class Update(StaffAuthorizedApi):
    """修改退貨單详情"""
    request = with_metaclass(RequestFieldSet)
    request.update_info = RequestField(DictField, desc = "退貨單更新", conf = {
        'id': IntField(desc = "退货单ID"),
        'code': CharField(desc = "設備編碼", is_required = False),
        'returns_num': CharField(desc = "订单号", is_required = False),
        'goods_name': CharField(desc = "商品名稱", is_required = False),
        'customer': CharField(desc = "客戶名稱", is_required = False),
        'quantity': IntField(desc = "商品数量" , is_required = False),
        'total_price': IntField(desc = "订单金额", is_required = False),
        'register_phone': CharField(desc = "註冊电话", is_required = False),
        'servicer': CharField(desc = "客服名稱", is_required = False),
        'channel_name': CharField(desc = "渠道名称", is_required = False),
        'shop_name': CharField(desc = "店铺名称", is_required = False),
        'cus_phone': CharField(desc = "客戶手機", is_required = False),
        'remark': CharField(desc = "備註", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "退貨單修改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        returns_num = request.update_info('returns_num')
        OrderReturnsServer.update(**request.update_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对退货单号为{id}的详情".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = returns_num)
        remark = "编辑退货单"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.UPDATE, record_detail, remark)
    def fill(self, response):
        return response

class Remove(StaffAuthorizedApi):
    """刪除退貨訂單"""
    request = with_metaclass(RequestFieldSet)
    request.remove_info = RequestField(DictField, desc = "用户详情", conf = {
        'code': CharField(desc = "设备编码"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "退貨訂單删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        code = request.remove_info['code']
        OrderReturnsServer.remove(**request.remove_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对SN号为{code}进行了退货操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = code)
        remark = "退货操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response

class Change(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.change_info = RequestField(DictField, desc = "用户详情", conf = {
        'code': CharField(desc = "设备编码"),
        'flag': CharField(desc = "识别码", choices = [('normal', "正常"), ('replace', "售后机"), ('patch', "补货")]),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "换货补货标记"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        code = request.change_info['code']
        flag = request.change_info['flag']
        OrderReturnsServer.change(**request.change_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 将SN号为：{code}状态标记为：{flag}".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = code, flag = flag)
        remark = "退货操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response

class Recover(StaffAuthorizedApi):
    '''恢复删除订单'''
    request = with_metaclass(RequestFieldSet)
    request.recover_info = RequestField(DictField, desc = "用户详情", conf = {
        'code': CharField(desc = "设备编码"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "退貨訂單恢复接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        code = request.recover_info['code']
        OrderReturnsServer.recover(**request.recover_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对SN号为{code}进行了恢复操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = code)
        remark = "退货恢复操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.RECOVER, record_detail, remark)
    def fill(self, response):
        return response
