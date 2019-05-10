# coding=UTF-8

# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''
import datetime

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.merchant.manager import MerchantServer, MerchantEquipmentServer
from tuoen.abs.service.equipment.manager import EquipmentSnServer
from tuoen.abs.service.service.manager import ServiceItemServer


class Add(StaffAuthorizedApi):
    """添加商户"""
    request = with_metaclass(RequestFieldSet)
    request.merchantId = RequestField(CharField, desc = "商户编号")
    request.merchantName = RequestField(CharField, desc = "商户名称")
    request.organId = RequestField(CharField, desc = "机构编号")
    request.organName = RequestField(CharField, desc = "机构名称")
    request.organLevel = RequestField(CharField, desc = "机构等级")
    request.realName = RequestField(CharField, desc = "真实姓名")
    request.idCard = RequestField(CharField, desc = "身份证号")
    request.phone = RequestField(CharField, desc = "手机号")
    request.regDate = RequestField(CharField, desc = "注册时间")
    request.serialNo = RequestField(CharField, desc = "硬件系列号")
    request.terminalId = RequestField(CharField, desc = "终端编号")
    request.bindingDate = RequestField(CharField, desc = "绑定时间")
    request.pid = RequestField(CharField, desc = "产品编号")


    response = with_metaclass(ResponseFieldSet)
    response.respCode = CharField(desc = "应答码")
    response.respMsg = CharField(desc = "应答描述")


    @classmethod
    def get_desc(cls):
        return "商户推送获取接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        merchant = MerchantServer.get_merchant_bymid(request.merchantId)
        if merchant is None:
            merchant_info = {"merchant_id":request.merchantId, "merchant_name":request.merchantName, \
                           "organ_id":request.organId, "organ_name":request.organName, \
                           "organ_level":request.organLevel, "real_name":request.realName, \
                           "id_card":request.idCard, "phone":request.phone, "pid":request.pid, \
                           "reg_date":datetime.datetime.strptime(request.regDate, '%Y%m%d%H%M%S'), \
                           "source":"ysb"}
        merchant = MerchantServer.generate(**merchant_info)
        serial_no_list = request.serialNo.split("|")
        terminal_id_list = request.terminalId.split("|")
        binding_date_list = request.bindingDate.split("|")
        merchant_equipment_list = []
        for i, value in enumerate(serial_no_list):
            equipment_sn = EquipmentSnServer.get_by_code(value)
            if equipment_sn is not None:
                service_item_qs = ServiceItemServer.search_qs(equipment_sn = equipment_sn)
                if service_item_qs.count() > 0:
                    service_item_qs[0].update(dsinfo_status = "yellow")
            merchant_equipment_list.append({"merchant":merchant, "equipment_sn":equipment_sn, \
                                            "serial_no":value, \
                                            "terminal_id":terminal_id_list[i], \
                                            "binding_date":datetime.datetime.strptime(binding_date_list[i], '%Y%m%d%H%M%S')})
        MerchantEquipmentServer.batch_generate(merchant_equipment_list)

    def fill(self, response):
        response.respCode = "0000"
        response.respMsg = "操作成功"
        return response
