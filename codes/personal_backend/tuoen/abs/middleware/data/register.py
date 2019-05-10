# coding=UTF-8
import json

from django.db.models import Q

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField
from model.store.model_import import ImportCustomerRegister, ImportStatus
from model.store.model_equipment_sn import EquipmentSn, SnStatusType
from model.store.model_equipment_register import EquipmentRegister, RegisterTypes
from model.store.model_service import ServiceItem
from model.store.model_equipment_out import EquipmentOut, AgentTypes


class RegisterImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportCustomerRegister

    def get_redis_name(self):
        return "ImportCustomerRegister"

    def get_fields(self):
        check_list = [
            ['agent_name', CharField(desc = "代理商名称")],
            ['code', CharField(desc = "客户编码")],
            ['phone', CharField(desc = "注册手机号")],
            ['name', CharField(desc = "客户姓名")],
            ['register_time', ExcelDateTimeField(desc = "客户注册时间")],
            ['bind_time', ExcelDateTimeField(desc = "绑定时间")],
            ['device_code', CharField(desc = "设备编码")],
        ]
        return check_list


    def convert_prepare(self, convert_list):
        customer_code_set = set()
        sn_set = set()

        for obj in convert_list:
            customer_code_set.add(obj.code)
            sn_set.add(obj.device_code)

        customer_code_list = list(customer_code_set)
        sn_list = list(sn_set)

        self._equipment_register_list = {register.code:register for register in \
                    EquipmentRegister.query().filter(code__in = customer_code_list)}
        self._equipment_sn_list = {equipment_sn.code:equipment_sn for equipment_sn in \
                                EquipmentSn.query().filter(code__in = sn_list)}
        return convert_list, []

    def skip_repeat(self, register):
        if not register.code:
            self._error_msg = "客户编码为空"
            return False

        if register.code in self._equipment_register_list:
            self._error_msg = "客户编码重复"
            return False

        return True

    def exec_convet(self, register):
        check_repeat = self.skip_repeat(register)
        if check_repeat:
            if register.device_code in self._equipment_sn_list:
                equipment_sn = self._equipment_sn_list[register.device_code]
                equipment_register = EquipmentRegister.create(equipment_sn = equipment_sn, agent_name = register.agent_name, \
                                         code = register.code, phone = register.phone, name = register.name, \
                                         register_time = register.register_time, bind_time = register.bind_time, \
                                         device_code = register.device_code, status = RegisterTypes.NORMAL)
                service_item_qs = ServiceItem.query(equipment_sn = equipment_sn)
                if service_item_qs.count() > 0:
                    service_item = service_item_qs[0]
                    service_item.update(dsinfo_status = SnStatusType.YELLOW)
            else:
                error_status = RegisterTypes.ABNORMAL
                equipment_out_qs = EquipmentOut.search(min_number__lte = register.device_code, \
                                     max_number__gte = register.device_code).filter(~Q(type = AgentTypes.SELF))
                if equipment_out_qs.count() > 0:
                    error_status = RegisterTypes.AGENT
                equipment_register = EquipmentRegister.create(agent_name = register.agent_name, \
                                         code = register.code, phone = register.phone, name = register.name, \
                                         register_time = register.register_time, bind_time = register.bind_time, \
                                         device_code = register.device_code, status = error_status)
                self._equipment_register_list[equipment_register.code] = equipment_register
            return True, ""

        return False, self._error_msg

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportCustomerRegister.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
