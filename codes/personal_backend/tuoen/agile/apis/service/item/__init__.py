# coding=UTF-8

# 环境的
import datetime
# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.security import Security
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, \
                                      BooleanField, DatetimeField, DateField, MobileField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.abs.middleware.department import department_middleware

from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.service.manager import ServiceServer, ServiceItemServer
from tuoen.abs.service.order.manager import OrderServer, StaffOrderEventServer
from tuoen.abs.service.customer.manager import CustomerServer
from tuoen.abs.service.equipment.manager import EquipmentRegisterServer
from tuoen.abs.service.authority import UserRightServer
from tuoen.abs.service.equipment.manager import EquipmentSnServer
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Search(StaffAuthorizedApi):
    """售后服务单产品列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        "equipment_code":CharField(desc = "设备编码", is_required = False),
        "equipment_code_status":CharField(desc = "设备编码状态", is_required = False),
        "seller_staff_id":IntField(desc = "售前客服id", is_required = False),
        "server_staff_id":IntField(desc = "售后客服id", is_required = False),
        "shop_id":CharField(desc = "店铺id", is_required = False),
        "buy_name":CharField(desc = "购买人姓名", is_required = False),
        "buy_mobile":CharField(desc = "购买人手机号", is_required = False),
        "remark":CharField(desc = "订单备注", is_required = False),
        "order_sn":CharField(desc = "订单号", is_required = False),
        "shop_name":IntField(desc = "店铺名称", is_required = False),
        "department_id":IntField(desc = "部门id", is_required = False),
        "buy_date_start":DateField(desc = "购买起始时间", is_required = False),
        "buy_date_end":DateField(desc = "购买结束时间", is_required = False),
        "dsinfo_status":BooleanField(desc = "是否开通(1:开通，0:未开通)", is_required = False),
        "rebate_status":BooleanField(desc = "是否激活(1:激活，0:未激活)", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '售后服务单产品列表', fmt = DictField(desc = "售后服务单产品列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "购买人", reprocess = Security.name_encryption),
        'phone': CharField(desc = "购买人电话", reprocess = Security.mobile_encryption),
        'equipment_status': CharField(desc = "设备状态"),
        'code': CharField(desc = "SN码"),
        'phone_code': CharField(desc = "手機編碼"),
        'pre_id': IntField(desc = "售前客服id"),
        'pre_name': CharField(desc = "售前客服"),
        'after_id': IntField(desc = "售后客服id"),
        'after_name': CharField(desc = "售后客服"),
        'department_name': CharField(desc = "部门名称"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'buy_time': DatetimeField(desc = "购买时间"),
        'remark': CharField(desc = "备注"),
        'order_sn':CharField(desc = "订单号"),
        'create_time': DatetimeField(desc = "录入时间"),
        'buyinfo_status': CharField(desc = "购买信息状态"),
        'dsinfo_status': CharField(desc = "电刷信息状态"),
        'rebate_status': CharField(desc = "激活信息状态"),
        'sn_status': CharField(desc = "设备码出入库状态"),
    }))

    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "售后服务单产品列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        if not user_pro._is_admin:
            request.search_info.update({"service__server_id__in": user_pro._staff_id_list})
            '''
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            request.search_info.update({"order__id__in": order_ids})
            '''
        if "equipment_code" in request.search_info:
            equipment_code = request.search_info.pop("equipment_code")
            request.search_info.update({"equipment_sn__code":equipment_code})
        if "equipment_code_status" in request.search_info:
            equipment_code_status = request.search_info.pop("equipment_code_status")
            request.search_info.update({"equipment_sn__sn_status":equipment_code_status})
        if "seller_staff_id" in request.search_info:
            seller_staff_id = request.search_info.pop("seller_staff_id")
            request.search_info.update({"service__seller_id":seller_staff_id})
        if "server_staff_id" in request.search_info:
            server_staff_id = request.search_info.pop("server_staff_id")
            request.search_info.update({"service__server_id":server_staff_id})
        if "shop_id" in request.search_info:
            shop_id = request.search_info.pop("shop_id")
            request.search_info.update({"order__shop_id":shop_id})
        if "buy_name" in request.search_info:
            buy_name = request.search_info.pop("buy_name")
            request.search_info.update({"order__consignee":buy_name})
        if "buy_mobile" in request.search_info:
            buy_mobile = request.search_info.pop("buy_mobile")
            request.search_info.update({"order__phone__contains":buy_mobile})
        if "remark" in request.search_info:
            remark = request.search_info.pop("remark")
            request.search_info.update({"order__remark__contains":remark})
        if "order_sn" in request.search_info:
            order_sn = request.search_info.pop("order_sn")
            request.search_info.update({"order__order_sn":order_sn})

        if 'department_id' in request.search_info:
            department_id = request.search_info.pop('department_id')
            department_ids = department_middleware.get_all_children_ids(department_id)
            department_ids.append(department_id)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            request.search_info.update({"order__id__in": order_ids})

        if "buy_date_start" in request.search_info:
            buy_date_start = request.search_info.pop("buy_date_start")
            request.search_info.update({"order__pay_time__gte":buy_date_start})
        if "buy_date_end" in request.search_info:
            buy_date_end = request.search_info.pop("buy_date_end")
            request.search_info.update({"order__pay_time__lte":\
                                datetime.datetime(buy_date_end.year, buy_date_end.month, buy_date_end.day, 23, 59, 59)})
        page_list = ServiceItemServer.search(request.current_page, **request.search_info)
        # 挂载售前售后客服
        ServiceServer.hung_staff_forservice(page_list.data)
        # 挂载部门
        StaffOrderEventServer.hung_department_byserviceitem(page_list.data)
        # 掛載手機編碼
        CustomerServer.hung_device_code(page_list.data)
        # 挂载店铺
        OrderServer.hung_shop_forservice(page_list.data)

        if self.auth_user.is_security:
            self.response.on_safe()

        return page_list

    def get_phone(self, service_item):
        phone = ""
        if service_item.order:
            if service_item.dsinfo_status != EquipmentSnServer.get_equipment_sn_status('red'):
                phone = MobileField.formatting(self, service_item.order.phone)
            else:
                phone = service_item.order.phone
        return phone

    def fill(self, response, page_list):
        response.data_list = [{
            'id': service_item.id,
            'name': service_item.order.consignee if service_item.order else "",
            'phone': self.get_phone(service_item),
            'code': service_item.equipment_sn.code if service_item.equipment_sn else "",
            'phone_code': service_item.phone_code,
            'equipment_status': service_item.equipment_sn.sn_status if service_item.equipment_sn else "",
            'pre_id': service_item.pre_staff.id if service_item.pre_staff else 0,
            'pre_name': service_item.pre_staff.name if service_item.pre_staff else "",
            'after_id': service_item.after_staff.id if service_item.after_staff else 0,
            'after_name': service_item.after_staff.name if service_item.after_staff else "",
            'department_name': service_item.department.name if service_item.department else "",
            'shop_id': service_item.shop.id if service_item.shop else 0,
            'shop_name': service_item.shop.name if service_item.shop else "",
            'buy_time': service_item.order.pay_time if service_item.order else "",
            'remark': service_item.order.remark if service_item.order else "",
            'order_sn':service_item.order.order_sn if service_item.order else "",
            'create_time': service_item.create_time,
            'buyinfo_status': service_item.buyinfo_status,
            'dsinfo_status': service_item.dsinfo_status,
            'rebate_status': service_item.rebate_status,
            'sn_status': service_item.sn_status,
        } for service_item in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response

class Statistics(StaffAuthorizedApi):
    """售后服务单统计"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        "equipment_code":CharField(desc = "设备编码", is_required = False),
        "equipment_code_status":CharField(desc = "设备编码状态", is_required = False),
        "seller_staff_id":IntField(desc = "售前客服id", is_required = False),
        "server_staff_id":IntField(desc = "售后客服id", is_required = False),
        "shop_id":CharField(desc = "店铺id", is_required = False),
        "buy_name":CharField(desc = "购买人姓名", is_required = False),
        "buy_mobile":CharField(desc = "购买人手机号", is_required = False),
        "remark":CharField(desc = "订单备注", is_required = False),
        "order_sn":CharField(desc = "订单号", is_required = False),
        "shop_id":IntField(desc = "店铺id", is_required = False),
        "department_id":IntField(desc = "部门id", is_required = False),
        "buy_date_start":DateField(desc = "购买起始时间", is_required = False),
        "buy_date_end":DateField(desc = "购买结束时间", is_required = False),
        "dsinfo_status":BooleanField(desc = "是否开通(1:开通，0:未开通)", is_required = False),
        "rebate_status":BooleanField(desc = "是否激活(1:激活，0:未激活)", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.sum_data = ResponseField(DictField, desc = "员工绩效统计", conf = {
        'volume': IntField(desc = "当日成交量"),
        'open_number': IntField(desc = "当日开通人数"),
        'open_rate': CharField(desc = "当日开通率"),
        'activation_number': IntField(desc = "当日激活人数"),
        'activation_rate': CharField(desc = "当日激活率"),
    })

    @classmethod
    def get_desc(cls):
        return "售后服务单统计接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        if not user_pro._is_admin:
            request.search_info.update({"service__server_id__in": user_pro._staff_id_list})

            '''
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            request.search_info.update({"order__id__in":order_ids})
            '''

        if "equipment_code" in request.search_info:
            equipment_code = request.search_info.pop("equipment_code")
            request.search_info.update({"equipment_sn__code":equipment_code})
        if "equipment_code_status" in request.search_info:
            equipment_code_status = request.search_info.pop("equipment_code_status")
            request.search_info.update({"equipment_sn__sn_status":equipment_code_status})
        if "seller_staff_id" in request.search_info:
            seller_staff_id = request.search_info.pop("seller_staff_id")
            request.search_info.update({"service__seller_id":seller_staff_id})
        if "server_staff_id" in request.search_info:
            server_staff_id = request.search_info.pop("server_staff_id")
            request.search_info.update({"service__server_id":server_staff_id})
        if "shop_id" in request.search_info:
            shop_id = request.search_info.pop("shop_id")
            request.search_info.update({"order__shop_id":shop_id})
        if "buy_name" in request.search_info:
            buy_name = request.search_info.pop("buy_name")
            request.search_info.update({"order__consignee":buy_name})
        if "buy_mobile" in request.search_info:
            buy_mobile = request.search_info.pop("buy_mobile")
            request.search_info.update({"order__phone__contains":buy_mobile})
        if "remark" in request.search_info:
            remark = request.search_info.pop("remark")
            request.search_info.update({"order__remark__contains":remark})
        if "order_sn" in request.search_info:
            order_sn = request.search_info.pop("order_sn")
            request.search_info.update({"order__order_sn":order_sn})

        if 'department_id' in request.search_info:
            department_id = request.search_info.pop('department_id')
            department_ids = department_middleware.get_all_children_ids(department_id)
            department_ids.append(department_id)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            request.search_info.update({"order__id__in": order_ids})

        if "buy_date_start" in request.search_info:
            buy_date_start = request.search_info.pop("buy_date_start")
            request.search_info.update({"order__pay_time__gte":buy_date_start})
        if "buy_date_end" in request.search_info:
            buy_date_end = request.search_info.pop("buy_date_end")
            request.search_info.update({"order__pay_time__lte":\
                                datetime.datetime(buy_date_end.year, buy_date_end.month, buy_date_end.day, 23, 59, 59)})

        sum_data = ServiceItemServer.alculation_by_searchinfo(**request.search_info)

        return sum_data

    def fill(self, response, sum_data):
        response.sum_data = {
            'volume': sum_data.volume_total,
            'open_number': sum_data.open_number_total,
            'open_rate': sum_data.open_rate_total,
            'activation_number': sum_data.activation_number_total,
            'activation_rate': sum_data.activation_rate_total,
        }
        return response


class Get(StaffAuthorizedApi):
    """售后服务单产品信息"""
    request = with_metaclass(RequestFieldSet)
    request.service_item_id = RequestField(IntField, desc = "售后服务单id")

    response = with_metaclass(ResponseFieldSet)
    response.service_item_info = ResponseField(DictField, desc = '售后服务单产品信息', conf = {
        'customer_id': IntField(desc = "客户id"),
        'customer_name': CharField(desc = "客户姓名"),
        'customer_phone': CharField(desc = "客户联系方式"),
        'device_code': CharField(desc = "设备编码"),
        'buy_date': DatetimeField(desc = "购买时间"),
        'wechat': CharField(desc = "微信号"),
        'nick': CharField(desc = "微信昵称"),
        'remark': CharField(desc = "备注"),

        'register_id': IntField(desc = "id"),
        'register_phone': CharField(desc = "注册手机号"),
        'register_name': CharField(desc = "注册姓名"),
    })

    @classmethod
    def get_desc(cls):
        return "售后服务单产品信息接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        service_item = ServiceItemServer.get(request.service_item_id)
        service = None
        if service_item.service:
            service = ServiceServer.get(service_item.service.id)
        equipment_register = EquipmentRegisterServer.get_register_byequipment(service_item.equipment)
        return service_item, service, equipment_register

    def fill(self, response, service_item, service, equipment_register):
        response.service_item_info = {
            'customer_id': service_item.customer.id if service_item.customer else 0,
            'customer_name': service_item.customer.name if service_item.customer else "",
            'customer_phone': service_item.customer.phone if service_item.customer else "",
            'device_code': service_item.equipment.code,
            'buy_date': service.order.pay_time if service_item.order else "",
            'wechat': service_item.customer.wechat if service_item.customer else "",
            'nick': service_item.customer.nick if service_item.customer else "",
            'remark': service.order.remark if service_item.order else "",

            'register_id': equipment_register.id if equipment_register else 0,
            'register_phone': equipment_register.phone if equipment_register else "",
            'register_name': equipment_register.name if equipment_register else "",
        }
        return response

class EditSn(StaffAuthorizedApi):
    """修改SN号"""
    request = with_metaclass(RequestFieldSet)
    request.sn_pre = RequestField(CharField, desc = '修改前的SN')
    request.sn_after = RequestField(CharField, desc = '修改后的SN')
    response = with_metaclass(ResponseFieldSet)
    response.exception_info = ResponseField(CharField, desc = '返回信息')

    @classmethod
    def get_desc(cls):
        return "SN修改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        res_info = ServiceItemServer.process_sn_change(request.sn_pre, request.sn_after)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 将SN:{sn_pre}修改为：{sn_after}".format(who = staff.name,
                                                                datetime = datetime.datetime.now().strftime(
                                                                "%Y-%m-%d %H:%M:%S"), sn_pre = request.sn_pre,
                                                                 sn_after = request.sn_after)
        remark = "SN号修改操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff,
                                   OperationTypes.STAFF, JournalTypes.EDIT, record_detail, remark)
        return res_info

    def fill(self, response, res_info):
        response.exception_info = res_info
        return response
