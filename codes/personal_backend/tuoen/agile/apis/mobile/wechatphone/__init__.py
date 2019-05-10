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

from tuoen.abs.middleware.department import department_middleware

from tuoen.abs.service.mobile.manager import MobilephoneServer
from tuoen.abs.service.mobile.manager import MobileDevicesServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer

import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Add(StaffAuthorizedApi):
    """添加手机信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_info = RequestField(DictField, desc = "注册手机信息", conf = {
        'leader': CharField(desc = "负责人姓名", is_required = False),
        'mobile_code': CharField(desc = "手机编号"),
        't_member': CharField(desc = "组员姓名", is_required = False),
        'wechat_nick': CharField(desc = "微信昵称", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'wechat_password': CharField(desc = "微信密码", is_required = False),
        'pay_password': CharField(desc = "微信支付密码", is_required = False),
        'wechat_remark': CharField(desc = "微信号备注", is_required = False),
        'department_id': IntField(desc = "部门id", is_required = False),
        'phone_number': CharField(desc = "手机号", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'name': CharField(desc = "实名人姓名", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
        'flow_card_number': CharField(desc = "流量卡号", is_required = False),
        'imei': CharField(desc = "手机imei号", is_required = False),
        'brand': CharField(desc = "手机品牌", is_required = False),
        'model': CharField(desc = "手机型号", is_required = False),
        'price': CharField(desc = "购买价格/分", is_required = False),
        'mobile_status': CharField(desc = "手机设备状态", is_required = False),
        'mobile_remark': CharField(desc = "手机设备备注", is_required = False),
        'phone_change': CharField(desc = "手机变更信息", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加手机信息接口"

    @classmethod
    def get_author(cls):
        return "fsy--"

    def execute(self, request):
        if 'department_id' in request.mobile_phone_info:
            department_id = request.mobile_phone_info.pop('department_id')
            department = department_middleware.get_self(department_id)
            request.mobile_phone_info.update({"department":department})
        mb_info = {}
        if 'mobile_status' in request.mobile_phone_info:
            mobile_status = request.mobile_phone_info.pop('mobile_status')
            mb_info.update({'status': mobile_status})
        if 'mobile_remark' in request.mobile_phone_info:
            mobile_remark = request.mobile_phone_info.pop('mobile_remark')
            mb_info.update({'remark': mobile_remark})
        if 'brand' in request.mobile_phone_info:
            brand = request.mobile_phone_info.pop('brand')
            mb_info.update({'brand': brand})
        if 'price' in request.mobile_phone_info:
            price = request.mobile_phone_info.pop('price')
            mb_info.update({'price': price})
        if 'imei' in request.mobile_phone_info:
            imei = request.mobile_phone_info.pop('imei')
            mb_info.update({'imei': imei})
        if 'mobile_code' in request.mobile_phone_info:
            mobile_code = request.mobile_phone_info.pop('mobile_code')
            mb_info.update({'code': mobile_code})
        if 'model' in request.mobile_phone_info:
            model = request.mobile_phone_info.pop('model')
            mb_info.update({'model': model})
        mobiledevice = MobileDevicesServer.generate(**mb_info)
        request.mobile_phone_info.update({"devices":mobiledevice})
        mobilephone = MobilephoneServer.generate(**request.mobile_phone_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 添加了手机编码为:{code}的条目".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), code = mobile_code)
        remark = "微信手机添加操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.ADD, record_detail, remark)
    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """手机详情列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'department_id': CharField(desc = "部门id", is_required = False),
        'phone_number': CharField(desc = "手机号码", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'mobile_code': CharField(desc = "手机编码", is_required = False),
        'wechat_nick': CharField(desc = "昵称", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机列表', fmt = DictField(desc = "手机列表", conf = {
        'id': IntField(desc = "手机Id"),
        'leader': CharField(desc = "组长姓名"),
        'mobile_code': CharField(desc = "手机编号"),
        't_member': CharField(desc = "组员姓名"),
        'wechat_nick': CharField(desc = "微信昵称"),
        'wechat_number': CharField(desc = "微信号"),
        'wechat_password': CharField(desc = "微信密码"),
        'pay_password': CharField(desc = "微信支付密码"),
        'wechat_remark': CharField(desc = "微信号备注"),
        'department_id': IntField(desc = "部门id"),
        'department_name': CharField(desc = "部门"),
        'phone_number': CharField(desc = "手机号"),
        'operator': CharField(desc = "运营商"),
        'real_name': CharField(desc = "实名人姓名"),
        'phone_remark': CharField(desc = "手机号备注"),
        'flow_card_number': CharField(desc = "流量卡号"),
        'imei': CharField(desc = "手机imei号"),
        'brand': CharField(desc = "手机品牌"),
        'model': CharField(desc = "手机型号"),
        'price': CharField(desc = "购买价格/分"),
        'mobile_status': CharField(desc = "手机设备状态"),
        'mobile_remark': CharField(desc = "手机设备备注"),
        'phone_change': CharField(desc = "手机变更信息"),
        # 'department_list': ListField(desc = '所属部门', fmt = DictField(desc = "部门信息", conf = {
        #    'department_id': IntField(desc = "部门id"),
        #    'department_name': CharField(desc = "部门名称"),
        # })),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "注册手机列表接口"

    @classmethod
    def get_author(cls):
        return "fsy_d"

    def execute(self, request):
        if 'department_id' in request.search_info:
            department_id = request.search_info.pop('department_id')
            request.search_info.update({'department_id': department_id})
        if 'wechat_nick' in request.search_info:
            wechat_nick = request.search_info.pop('wechat_nick')
            request.search_info.update({'wechat_nick__contains': wechat_nick})
        if 'wechat_number' in request.search_info:
            wechat_number = request.search_info.pop('wechat_number')
            request.search_info.update({'wechat_number': wechat_number})
        if 'phone_number' in request.search_info:
            phone_number = request.search_info.pop('phone_number')
            request.search_info.update({'phone_number': phone_number})
        if 'mobile_code' in request.search_info:
            code = request.search_info.pop('mobile_code')
            request.search_info.update({'devices__code': code})
        mobilephone_page = MobilephoneServer.search_new(request.current_page, **request.search_info)
        # 挂载手机设备信息
        # 挂载leader&staff
        # MobilephoneServer.hung_leader_staff(mobilephone_page.data)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 进行了微信手机盘点查询操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "微信手机查询操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.LOOK, record_detail, remark)
        return mobilephone_page

    def fill(self, response, mobilephone_page):
        response.data_list = [{
            'id': mobilephone.id,
            'leader': mobilephone.leader,
            'mobile_code': mobilephone.devices.code if mobilephone.devices else "",
            't_member': mobilephone.t_member,
            'wechat_nick': mobilephone.wechat_nick,
            'wechat_number': mobilephone.wechat_number,
            'wechat_password': mobilephone.wechat_password,
            'pay_password': mobilephone.pay_password,
            'wechat_remark': mobilephone.wechat_remark,
            'department_id': mobilephone.department.id if mobilephone.department else 0,
            'department_name': mobilephone.department.name if mobilephone.department else "",
            'phone_number': mobilephone.phone_number,
            'operator': mobilephone.operator,
            'real_name': mobilephone.staff.name if mobilephone.staff else "",
            'phone_remark': mobilephone.phone_remark,
            'flow_card_number': mobilephone.flow_card_number,
            'imei': mobilephone.devices.imei if mobilephone.devices else "",
            'brand': mobilephone.devices.brand if mobilephone.devices else "",
            'model': mobilephone.devices.model if mobilephone.devices else "",
            'price': mobilephone.devices.price if mobilephone.devices else "",
            'mobile_status': mobilephone.status,
            'mobile_remark': mobilephone.phone_remark,
            'phone_change': mobilephone.phone_change,
            } for mobilephone in mobilephone_page.data]
        response.total = mobilephone_page.total
        response.total_page = mobilephone_page.total_page
        return response

class Update(StaffAuthorizedApi):
    """修改手机信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_id = RequestField(IntField, desc = '手机id')
    request.mobile_phone_info = RequestField(DictField, desc = "手机详情", conf = {
        'leader': CharField(desc = "负责人姓名", is_required = False),
        'mobile_code': CharField(desc = "手机编码", is_required = False),
        't_member': CharField(desc = "组员姓名", is_required = False),
        'wechat_nick': CharField(desc = "微信昵称", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'wechat_password': CharField(desc = "微信密码", is_required = False),
        'pay_password': CharField(desc = "微信支付密码", is_required = False),
        'wechat_remark': CharField(desc = "微信号备注", is_required = False),
        'department_id': IntField(desc = "部门", is_required = False),
        'phone_number': CharField(desc = "手机号", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'name': CharField(desc = "实名人姓名", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
        'flow_card_number': CharField(desc = "流量卡号", is_required = False),
        'imei': CharField(desc = "手机imei号", is_required = False),
        'brand': CharField(desc = "手机品牌", is_required = False),
        'model': CharField(desc = "手机型号", is_required = False),
        'price': CharField(desc = "购买价格/分", is_required = False),
        'mobile_status': CharField(desc = "手机设备状态", is_required = False),
        'mobile_remark': CharField(desc = "手机设备备注", is_required = False),
        'phone_change': CharField(desc = "手机变更信息", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改手机信息接口"

    @classmethod
    def get_author(cls):
        return "fsy--"

    def execute(self, request):
        mb_info = {}
        if 'mobile_status' in request.mobile_phone_info:
            mobile_status = request.mobile_phone_info.pop('mobile_status')
            mb_info.update({'status': mobile_status})
        if 'mobile_remark' in request.mobile_phone_info:
            mobile_remark = request.mobile_phone_info.pop('mobile_remark')
            mb_info.update({'remark': mobile_remark})
        if 'brand' in request.mobile_phone_info:
            brand = request.mobile_phone_info.pop('brand')
            mb_info.update({'brand': brand})
        if 'price' in request.mobile_phone_info:
            price = request.mobile_phone_info.pop('price')
            mb_info.update({'price': price})
        if 'imei' in request.mobile_phone_info:
            imei = request.mobile_phone_info.pop('imei')
            mb_info.update({'imei': imei})
        if 'mobile_code' in request.mobile_phone_info:
            mobile_code = request.mobile_phone_info.pop('mobile_code')
            mb_info.update({'code': mobile_code})
        if 'model' in request.mobile_phone_info:
            model = request.mobile_phone_info.pop('model')
            mb_info.update({'model': model})
        MobileDevicesServer.update_new(request.mobile_phone_id, **mb_info)

        if 'department_id' in request.mobile_phone_info:
            department_id = request.mobile_phone_info.pop('department_id')
            department = department_middleware.get_self(department_id)
            request.mobile_phone_info.update({"department":department})

        MobilephoneServer.update_new(request.mobile_phone_id, **request.mobile_phone_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对微信手机盘点表中条目{id}进行了更新.".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = request.mobile_phone_id)
        remark = "微信手机添加操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.UPDATE, record_detail, remark)
    def fill(self, response):
        return response


class RemoveAll(StaffAuthorizedApi):
    """删除手机信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_id = RequestField(IntField, desc = "注册手机id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "注册手机删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        MobilephoneServer.remove_all(request.mobile_phone_id)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 删除了微信手机盘点表中条目{id}.".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = request.mobile_phone_id)
        remark = "微信手机删除操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.DELETE, record_detail, remark)
    def fill(self, response):
        return response
