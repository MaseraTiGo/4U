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
from tuoen.abs.service.mobile.manager import MobileMaintainServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer


class Add(StaffAuthorizedApi):
    """添加手机设备维护关系"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_maintain_info = RequestField(DictField, desc = "手机设备维护信息", conf = {
        'mobile_devices_id':IntField(desc = "手机设备id"),
        'staff_id': IntField(desc = "员工id"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备维护关系添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = StaffServer.get(request.mobile_maintain_info["staff_id"])
        request.mobile_maintain_info.update({"staff": staff})

        mobile_devices = MobileDevicesServer.get(request.mobile_maintain_info["mobile_devices_id"])
        request.mobile_maintain_info.update({"devices": mobile_devices})

        MobileMaintainServer.is_maintain_exist(mobile_devices)
        MobileMaintainServer.generate(**request.mobile_maintain_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """手机设备维护列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'keyword': CharField(desc = "关键词(手机编码或姓名)", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '机设备维护列表', fmt = DictField(desc = "机设备维护列表", conf = {
        'id': IntField(desc = "id"),
        'mobile_devices_id': IntField(desc = "手机设备id"),
        'mobile_devices_code': CharField(desc = "手机设备编码"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'is_working': BooleanField(desc = "是否在职"),
        'remark': CharField(desc = "备注"),
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
        return "手机设备维护列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilemaintain_page = MobileMaintainServer.search(request.current_page, **request.search_info)
        for mobilemaintain in mobilemaintain_page.data:
            if mobilemaintain.staff is not None:
                mobilemaintain.staff = StaffPermiseServer.hung_permise_bystaff(mobilemaintain.staff)

        return mobilemaintain_page

    def fill(self, response, mobilemaintain_page):
        response.data_list = [{
            'id': mobilemaintain.id,
            'mobile_devices_id': mobilemaintain.devices.id,
            'mobile_devices_code': mobilemaintain.devices.code,
            'staff_id': mobilemaintain.staff.id,
            'staff_name': mobilemaintain.staff.name,
            'is_working': mobilemaintain.staff.is_working,
            'remark': mobilemaintain.remark,
            'create_time': mobilemaintain.create_time,
            'department_list':[{
               'department_id':department.id,
               'department_name':department.name
               } for department in mobilemaintain.staff.department_list] if mobilemaintain.staff else []
        } for mobilemaintain in mobilemaintain_page.data]
        response.total = mobilemaintain_page.total
        response.total_page = mobilemaintain_page.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取手机设备维护详情"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_maintain_id = RequestField(IntField, desc = 'id')

    response = with_metaclass(ResponseFieldSet)
    response.mobile_maintain_info = ResponseField(DictField, desc = "手机设备维护详情", conf = {
        'id': IntField(desc = "id"),
        'mobile_devices_id': IntField(desc = "手机设备id"),
        'mobile_devices_code': CharField(desc = "手机设备编码"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'is_working': BooleanField(desc = "是否在职"),
        'remark': CharField(desc = "备注"),
        'create_time': CharField(desc = "添加时间"),
        'department_list': ListField(desc = '所属部门', fmt = DictField(desc = "部门信息", conf = {
           'department_id': IntField(desc = "部门id"),
           'department_name': CharField(desc = "部门名称"),
        })),
    })

    @classmethod
    def get_desc(cls):
        return "手机设备维护详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilemaintain = MobileMaintainServer.get(request.mobile_maintain_id)
        mobilemaintain.staff = StaffPermiseServer.hung_permise_bystaff(mobilemaintain.staff)

        return mobilemaintain

    def fill(self, response, mobilemaintain):
        response.mobile_maintain_info = {
            'id': mobilemaintain.id,
            'mobile_devices_id': mobilemaintain.devices.id,
            'mobile_devices_code': mobilemaintain.devices.code,
            'staff_id': mobilemaintain.staff.id,
            'staff_name': mobilemaintain.staff.name,
            'is_working': mobilemaintain.staff.is_working,
            'remark': mobilemaintain.remark,
            'create_time': mobilemaintain.create_time,
            'department_list':[{
               'department_id':department.id,
               'department_name':department.name
               } for department in mobilemaintain.staff.department_list]
        }
        return response


class Update(StaffAuthorizedApi):
    """修改手机设备维护信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_maintain_id = RequestField(IntField, desc = 'id')
    request.mobile_maintain_info = RequestField(DictField, desc = "手机设备维护详情", conf = {
        'mobile_devices_id':IntField(desc = "手机设备id"),
        'staff_id': IntField(desc = "员工id"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备维护信息修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        mobilemaintain = MobileMaintainServer.get(request.mobile_maintain_id)

        staff = StaffServer.get(request.mobile_maintain_info["staff_id"])
        request.mobile_maintain_info.update({"staff": staff})

        mobile_devices = MobileDevicesServer.get(request.mobile_maintain_info["mobile_devices_id"])
        request.mobile_maintain_info.update({"devices": mobile_devices})

        MobileMaintainServer.is_maintain_exist(mobile_devices, mobilemaintain)

        MobileMaintainServer.update(mobilemaintain, **request.mobile_maintain_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除手机设备维护信息"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_maintain_id = RequestField(IntField, desc = "id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备维护信息删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        MobileMaintainServer.remove(request.mobile_maintain_id)

    def fill(self, response):
        return response
