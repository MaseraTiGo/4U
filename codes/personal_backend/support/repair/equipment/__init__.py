# coding=UTF-8

from model.store.model_equipment import Equipment
from model.store.model_equipment_sn import EquipmentSn
from model.store.model_service import ServiceItem
from model.store.model_equipment_register import EquipmentRegister

class EquipmentRepair(object):

    def run(self):
        self.ready()
        i = 0
        equipment_qs = Equipment.search()
        print("==========设备数：", len(equipment_qs))

        for equipment in equipment_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)
            equipment_sn = EquipmentSn.create(customer = equipment.customer, equipment = equipment, sn_status = equipment.equipment_status, \
                                              order = equipment.order, product = equipment.product, product_model = equipment.product_model, code = equipment.code, \
                                              last_cal_time = equipment.last_cal_time, total_amount = equipment.total_amount, \
                                              update_time = equipment.update_time, create_time = equipment.create_time)
            if equipment in self._all_service_item:
                service_item = self._all_service_item[equipment]
                service_item.update(equipment_sn = equipment_sn)
            if equipment in self._all_equipment_register:
                equipment_register = self._all_equipment_register[equipment]
                equipment_register.update(equipment_sn = equipment_sn)


    def ready(self):
        self._all_service_item = {}
        self._all_equipment_register = {}
        service_item_qs = ServiceItem.search()
        print("=====售后服务单数据数=====", len(service_item_qs))
        for service_item in service_item_qs:
            self._all_service_item[service_item.equipment] = service_item

        equipment_register_qs = EquipmentRegister.search()
        print("=====设备注册数据数=====", len(equipment_register_qs))
        for equipment_register in equipment_register_qs:
            if equipment_register.equipment:
                self._all_equipment_register[equipment_register.equipment] = equipment_register

        print("=====数据准备完成=====")

