# coding=UTF-8

import json

from model.store.model_equipment_sn import EquipmentSn
from model.store.model_equipment_register import EquipmentRegister, RegisterTypes
from model.store.model_equipment_out import EquipmentOut, AgentTypes


class RegisterRepair():

    def run(self):
        self.ready()

        i = 0
        # equipment_register_qs = EquipmentRegister.search()
        for key, value in self._all_equipment_register.items():
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)
            if key in self._all_equipment_sn:
                if not value.device_code:
                    value.update(device_code = self._all_equipment_sn[key].code)

        print("===重复条数===", n)


    def ready(self):
        self._all_equipment_sn = {}
        self._all_equipment_register = {}

        equipment_sn_qs = EquipmentSn.search()
        print("=====SN数=====", len(equipment_sn_qs))
        for equipment_sn in equipment_sn_qs:
            self._all_equipment_sn[equipment_sn.id] = equipment_sn

        equipment_register_qs = EquipmentRegister.search()
        print("=====SN注册数=====", len(equipment_register_qs))
        for equipment_register in equipment_register_qs:
            self._all_equipment_register[equipment_register.equipment_sn_id] = equipment_register

        print("=====数据准备完成=====")

    '''
    def run(self):
        i = 0
        equipment_register_qs = EquipmentRegister.search()
        for equipment_register in equipment_register_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)
            if not equipment_register.equipment_sn_id:
                if equipment_register.device_code:
                    register_type = self.calculation_equipment_out_type(equipment_register.device_code)
                    equipment_register.update(status = register_type)
            else:
                if not equipment_register.equipment_sn.customer_id:
                    if equipment_register.equipment_sn.code:
                        register_type = self.calculation_equipment_out_type(equipment_register.equipment_sn.code)
                        equipment_register.update(status = register_type)

        print("===结束===")


    def calculation_equipment_out_type(self, device_code):
        equipment_out_qs = EquipmentOut.search(min_number__lte = device_code, max_number__gte = device_code)
        if equipment_out_qs.count() > 0:
            equipment_out = equipment_out_qs[0]
            return self.register_type(equipment_out.type)
        else:
            return RegisterTypes.ABNORMAL

    def register_type(self, type):
        if type == AgentTypes.SELF:
            # return RegisterTypes.NORMAL
            return RegisterTypes.ABNORMAL
        else:
            return RegisterTypes.AGENT
    '''
