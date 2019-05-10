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
from tuoen.abs.service.equipment.manager import EquipmentRegisterServer
from tuoen.abs.service.service.manager import ServiceItemServer


class Update(StaffAuthorizedApi):
    """修改设备注册信息"""
    request = with_metaclass(RequestFieldSet)
    request.equipment_register_id = RequestField(IntField, desc = '设备注册id')
    request.equipment_register_info = RequestField(DictField, desc = "设备注册详情", conf = {
        'name': CharField(desc = "注册姓名"),
        'phone': CharField(desc = "注册手机号"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改设备注册信息接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       equipment_register = EquipmentRegisterServer.get(request.equipment_register_id)
       EquipmentRegisterServer.update(equipment_register, **request.equipment_register_info)
       if not ("*" in request.equipment_register_info["name"] or "*" in request.equipment_register_info["phone"]):
           service_item = ServiceItemServer.get_serviceitem_byequipment(equipment_register.equipment_sn)
           print("----------")
           if service_item is not None:
               print("----------111111")
               ServiceItemServer.update(service_item, dsinfo_status = "green")

    def fill(self, response):
        return response
