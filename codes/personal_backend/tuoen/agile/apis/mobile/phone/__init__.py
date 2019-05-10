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
from tuoen.abs.service.mobile.manager import MobilephoneServer
from tuoen.abs.service.mobile.manager import MobileDevicesServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer


class Add(StaffAuthorizedApi):
    """添加注册手机"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_info = RequestField(DictField, desc = "注册手机信息", conf = {
        'phone_number': CharField(desc = "手机号"),
        'staff_id': IntField(desc = "员工id", is_required = False),
        'mobile_devices_id': IntField(desc = "手机设备id", is_required = False),
        'name': CharField(desc = "姓名", is_required = False),
        'identity': CharField(desc = "身份证", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'rent': IntField(desc = "月租", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
        'tag': CharField(desc = "标签", is_required = False),
        'status': CharField(desc = "注册手机状态('normal':正常,'frozen':冻结,'seal':封号,\
                            'arrears':欠费,'discontinuation':停用,'other':其它,)", is_required = False),
        'flow_card_number': CharField(desc = "流量卡号", is_required = False),
        'card_password': CharField(desc = "手机卡密码", is_required = False),
        'phone_change': CharField(desc = "手机号变更信息", is_required = False),
        'wechat_nick': CharField(desc = "微信昵称", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'wechat_password': CharField(desc = "微信密码", is_required = False),
        'wechat_remark': CharField(desc = "微信备注", is_required = False),
        'pay_password': CharField(desc = "支付密码", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加注册手机接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        MobilephoneServer.is_phone_exist(request.mobile_phone_info["phone_number"])
        if 'staff_id' in request.mobile_phone_info:
            staff = StaffServer.get(request.mobile_phone_info["staff_id"])
            request.mobile_phone_info.update({"staff": staff})
            request.mobile_phone_info.update({"name": staff.name})
            request.mobile_phone_info.update({"identity": staff.identity})
        if 'mobile_devices_id' in request.mobile_phone_info:
            mobile_devices = MobileDevicesServer.get(request.mobile_phone_info["mobile_devices_id"])
            request.mobile_phone_info.update({"devices": mobile_devices})
        mobilephone = MobilephoneServer.generate(**request.mobile_phone_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """手机列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'keyword': CharField(desc = "关键词(姓名或手机号)", is_required = False),
        'mobile_code': CharField(desc = "设备码", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机列表', fmt = DictField(desc = "手机列表", conf = {
        'id': IntField(desc = "手机id"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'is_working': BooleanField(desc = "是否在职"),
        'identity': CharField(desc = "身份证"),
        'mobile_devices_id': CharField(desc = "手机设备id"),
        'mobile_devices_code': CharField(desc = "手机设备编号"),
        'phone_number': CharField(desc = "手机号"),
        'operator': CharField(desc = "运营商"),
        'rent': IntField(desc = "租金"),
        'phone_remark': CharField(desc = "手机号备注"),
        'tag': CharField(desc = "标签"),
        'flow_card_number': CharField(desc = "流量卡号"),
        'card_password': CharField(desc = "手机卡密码"),
        'phone_change': CharField(desc = "手机号变更信息"),
        'wechat_nick': CharField(desc = "微信昵称"),
        'wechat_number': CharField(desc = "微信号"),
        'wechat_password': CharField(desc = "微信密码"),
        'wechat_remark': CharField(desc = "微信备注"),
        'pay_password': CharField(desc = "支付密码"),
        'status': CharField(desc = "手机号状态（normal:正常，frozen:冻结，seal:封号，arrears:欠费,discontinuation:停用,other:其它）"),
        'create_time': DatetimeField(desc = "添加时间"),
        'department_list': ListField(desc = '所属部门', fmt = DictField(desc = "部门信息", conf = {
           'department_id': IntField(desc = "部门id"),
           'department_name': CharField(desc = "部门名称"),
        })),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "注册手机列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilephone_page = MobilephoneServer.search(request.current_page, **request.search_info)
        for mobilephone in mobilephone_page.data:
            if mobilephone.staff is not None:
                mobilephone.staff = StaffPermiseServer.hung_permise_bystaff(mobilephone.staff)

        return mobilephone_page

    def fill(self, response, mobilephone_page):
        response.data_list = [{
            'id': mobilephone.id,
            'staff_id': mobilephone.staff.id if mobilephone.staff else 0,
            'staff_name': mobilephone.name,
            'is_working': mobilephone.staff.is_working if mobilephone.staff else "",
            'identity': mobilephone.identity,
            'mobile_devices_id': mobilephone.devices.id if mobilephone.devices else 0,
            'mobile_devices_code': mobilephone.devices.code if mobilephone.devices else "",
            'phone_number': mobilephone.phone_number,
            'operator': mobilephone.operator,
            'rent': mobilephone.rent,
            'phone_remark': mobilephone.phone_remark,
            'tag': mobilephone.tag,
            'flow_card_number': mobilephone.flow_card_number,
            'card_password': mobilephone.card_password,
            'phone_change': mobilephone.phone_change,
            'wechat_nick': mobilephone.wechat_nick,
            'wechat_number': mobilephone.wechat_number,
            'wechat_password': mobilephone.wechat_password,
            'wechat_remark': mobilephone.wechat_remark,
            'pay_password': mobilephone.pay_password,
            'status': mobilephone.status,
            'create_time': mobilephone.create_time,
            'department_list':[{
               'department_id':department.id,
               'department_name':department.name
               } for department in mobilephone.staff.department_list] if mobilephone.staff else []
        } for mobilephone in mobilephone_page.data]
        response.total = mobilephone_page.total
        response.total_page = mobilephone_page.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取注册手机详情"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_id = RequestField(IntField, desc = '手机id')

    response = with_metaclass(ResponseFieldSet)
    response.mobile_phone_info = ResponseField(DictField, desc = "账号列表", conf = {
        'id': IntField(desc = "手机id"),
        'name': CharField(desc = "员工姓名"),
        'is_working': IntField(desc = "是否在职"),
        'identity': CharField(desc = "身份证"),
        'code': CharField(desc = "手机编号"),
        'phone_number': CharField(desc = "手机号"),
        'operator': CharField(desc = "运营商"),
        'rent': IntField(desc = "租金"),
        'phone_remark': CharField(desc = "手机号备注备注"),
        'tag': CharField(desc = "标签"),
        'flow_card_number': CharField(desc = "流量卡号"),
        'card_password': CharField(desc = "手机卡密码"),
        'phone_change': CharField(desc = "手机号变更信息"),
        'wechat_nick': CharField(desc = "微信昵称"),
        'wechat_number': CharField(desc = "微信号"),
        'wechat_password': CharField(desc = "微信密码"),
        'wechat_remark': CharField(desc = "微信备注"),
        'pay_password': CharField(desc = "支付密码"),
        'create_time': DatetimeField(desc = "添加时间"),
        'department_list': ListField(desc = '所属部门', fmt = DictField(desc = "部门信息", conf = {
           'department_id': IntField(desc = "部门id"),
           'department_name': CharField(desc = "部门名称"),
        })),
    })

    @classmethod
    def get_desc(cls):
        return "注册手机详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilephone = MobilephoneServer.get(request.mobile_phone_id)
        mobilephone.staff = StaffPermiseServer.hung_permise_bystaff(mobilephone.staff)

        return mobilephone

    def fill(self, response, mobilephone):
        response.mobile_phone_info = {
            'id': mobilephone.id,
            'code': mobilephone.devices.code if mobilephone.devices else "",
            'name': mobilephone.name,
            'is_working': mobilephone.staff.is_working if mobilephone.staff else "",
            'identity': mobilephone.identity,
            'phone_number': mobilephone.phone_number,
            'operator': mobilephone.operator,
            'rent': mobilephone.rent,
            'remark': mobilephone.remark,
            'tag': mobilephone.tag,
            'flow_card_number': mobilephone.flow_card_number,
            'card_password': mobilephone.card_password,
            'phone_change': mobilephone.phone_change,
            'wechat_nick': mobilephone.wechat_nick,
            'wechat_number': mobilephone.wechat_number,
            'wechat_password': mobilephone.wechat_password,
            'wechat_remark': mobilephone.wechat_remark,
            'pay_password': mobilephone.pay_password,
            'create_time': mobilephone.create_time,
            'department_list':[{
               'department_id':department.id,
               'department_name':department.name
               } for department in mobilephone.staff.department_list]
        }
        return response


class Update(StaffAuthorizedApi):
    """修改手机号信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_id = RequestField(IntField, desc = '手机id')
    request.mobile_phone_info = RequestField(DictField, desc = "手机详情", conf = {
        'staff_id': IntField(desc = "员工id", is_required = False),
        'mobile_devices_id': CharField(desc = "手机设备id", is_required = False),
        'phone_number': CharField(desc = "手机号"),
        'name': CharField(desc = "姓名", is_required = False),
        'identity': CharField(desc = "身份证", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'rent': IntField(desc = "月租", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
        'tag': CharField(desc = "标签", is_required = False),
        'status': CharField(desc = "注册手机状态('normal':正常,'frozen':冻结,'seal':封号,\
                            'arrears':欠费,'discontinuation':停用,'other':其它,)", is_required = False),
        'flow_card_number': CharField(desc = "流量卡号", is_required = False),
        'card_password': CharField(desc = "手机卡密码", is_required = False),
        'phone_change': CharField(desc = "手机号变更信息", is_required = False),
        'wechat_nick': CharField(desc = "微信昵称", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'wechat_password': CharField(desc = "微信密码", is_required = False),
        'wechat_remark': CharField(desc = "微信备注", is_required = False),
        'pay_password': CharField(desc = "支付密码", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改注册手机接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilephone = MobilephoneServer.get(request.mobile_phone_id)
        MobilephoneServer.is_phone_exist(request.mobile_phone_info["phone_number"], mobilephone)
        if "staff_id" in request.mobile_phone_info:
            staff = StaffServer.get(request.mobile_phone_info["staff_id"])
            request.mobile_phone_info.update({"staff":staff})
            request.mobile_phone_info.update({"name":staff.name})
            request.mobile_phone_info.update({"identity":staff.identity})
        else:
            request.mobile_phone_info.update({"staff":None})

        if "mobile_devices_id" in request.mobile_phone_info:
            mobile_devices = MobileDevicesServer.get(request.mobile_phone_info["mobile_devices_id"])
            request.mobile_phone_info.update({"devices":mobile_devices})
        else:
            request.mobile_phone_info.update({"devices":None})

        MobilephoneServer.update(mobilephone, **request.mobile_phone_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除注册手机"""
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
        MobilephoneServer.remove(request.mobile_phone_id)

    def fill(self, response):
        return response
