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
from tuoen.abs.service.mobile.manager import MobileDevicesServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer


class Add(StaffAuthorizedApi):
    """添加手机设备"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_devices_info = RequestField(DictField, desc = "手机设备信息", conf = {
        'code': CharField(desc = "手机设备编码"),
        'brand': CharField(desc = "手机品牌", is_required = False),
        'model': CharField(desc = "手机型号", is_required = False),
        'price': IntField(desc = "购买价格/分", is_required = False),
        'imei': CharField(desc = "手机imei号", is_required = False),
        'status': CharField(desc = "手机设备状态(normal:正常,scrap:报废,idle:闲置,other:其它)", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加手机设备"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        MobileDevicesServer.is_code_exist(request.mobile_devices_info["code"])
        MobileDevicesServer.generate(**request.mobile_devices_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """手机设备列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "手机设备编码", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机设备列表', fmt = DictField(desc = "手机列表", conf = {
        'id': IntField(desc = "id"),
        'code': CharField(desc = "手机设备编码"),
        'brand': CharField(desc = "手机品牌"),
        'model': CharField(desc = "手机型号"),
        'price': IntField(desc = "购买价格/分"),
        'status': CharField(desc = "手机设备状态"),
        'imei': CharField(desc = "手机imei号"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "添加时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "手机设备列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobile_devices_page = MobileDevicesServer.search(request.current_page, **request.search_info)

        return mobile_devices_page

    def fill(self, response, mobile_devices_page):
        response.data_list = [{
            'id': mobile_devices.id,
            'code': mobile_devices.code,
            'brand': mobile_devices.brand,
            'model': mobile_devices.model,
            'price': mobile_devices.price,
            'status': mobile_devices.status,
            'imei': mobile_devices.imei,
            'remark': mobile_devices.remark,
            'create_time': mobile_devices.create_time,
        } for mobile_devices in mobile_devices_page.data]
        response.total = mobile_devices_page.total
        response.total_page = mobile_devices_page.total_page
        return response


class Searchall(StaffAuthorizedApi):
    """手机设备列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机设备列表', fmt = DictField(desc = "手机列表", conf = {
        'id': IntField(desc = "id"),
        'code': CharField(desc = "手机设备编码"),
    }))

    @classmethod
    def get_desc(cls):
        return "手机设备全部列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobile_devices_list = MobileDevicesServer.searchall(**request.search_info)

        return mobile_devices_list

    def fill(self, response, mobile_devices_list):
        response.data_list = [{
            'id': mobile_devices.id,
            'code': mobile_devices.code,
        } for mobile_devices in mobile_devices_list]
        return response


class Get(StaffAuthorizedApi):
    """获取手机设备详情"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_devices_id = RequestField(IntField, desc = '手机id')

    response = with_metaclass(ResponseFieldSet)
    response.mobile_devices_info = ResponseField(DictField, desc = "手机设备信息", conf = {
        'id': IntField(desc = "id"),
        'code': CharField(desc = "手机设备编码"),
        'brand': CharField(desc = "手机品牌"),
        'model': CharField(desc = "手机型号"),
        'price': IntField(desc = "购买价格/分"),
        'status': CharField(desc = "手机设备状态"),
        'imei': CharField(desc = "手机imei号"),
        'remark': CharField(desc = "备注"),
    })

    @classmethod
    def get_desc(cls):
        return "手机设备详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobile_devices = MobileDevicesServer.get(request.mobile_devices_id)

        return mobile_devices

    def fill(self, response, mobile_devices):
        response.mobile_devices_info = {
            'id': mobile_devices.id,
            'code': mobile_devices.code,
            'brand': mobile_devices.brand,
            'model': mobile_devices.model,
            'price': mobile_devices.price,
            'status': mobile_devices.status,
            'imei': mobile_devices.imei,
            'remark': mobile_devices.remark,
        }
        return response


class Update(StaffAuthorizedApi):
    """修改手机设备信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_devices_id = RequestField(IntField, desc = 'id')
    request.mobile_devices_info = RequestField(DictField, desc = "手机设备详情", conf = {
        'code': CharField(desc = "手机设备编码"),
        'brand': CharField(desc = "手机品牌", is_required = False),
        'model': CharField(desc = "手机型号", is_required = False),
        'price': IntField(desc = "购买价格/分", is_required = False),
        'imei': IntField(desc = "手机imei号", is_required = False),
        'status': CharField(desc = "手机设备状态(normal:正常,scrap:报废,idle:闲置,other:其它)", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改手机设备接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobile_devices = MobileDevicesServer.get(request.mobile_devices_id)
        MobileDevicesServer.is_code_exist(request.mobile_devices_info["code"], mobile_devices)
        MobileDevicesServer.update(mobile_devices, **request.mobile_devices_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除手机设备"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_devices_id = RequestField(IntField, desc = "id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobile_devices = MobileDevicesServer.get(request.mobile_devices_id)
        MobileDevicesServer.remove(mobile_devices)

    def fill(self, response):
        return response
