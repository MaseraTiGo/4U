# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from tuoen.abs.service.equipment.register import EquipmentRegisterHelper

from model.store.model_equipment import Equipment, EquipmentStatusType
from model.store.model_equipment_sn import EquipmentSn, SnStatusType


class EquipmentServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询设备列表"""

        equipment_qs = Equipment.search(**search_info)

        equipment_qs.order_by("-create_time")
        return Splitor(current_page, equipment_qs)

    @classmethod
    def hung_code_bylogistics(cls, logistics_list):
        """根据物流详情挂载设备"""
        for logistics in logistics_list:
            for logisticsitem in logistics.items:
                equipment_qs = Equipment.search(logistics_item = logisticsitem)
                logisticsitem.equipment_list = equipment_qs

        return logistics_list

    @classmethod
    def get_equipment_status(cls, status):
        if status == "red":
            return EquipmentStatusType.RED
        elif status == "yellow":
            return EquipmentStatusType.YELLOW
        elif status == "green":
            return EquipmentStatusType.GREEN
        elif status == "tgreen":
            return EquipmentStatusType.TGREEB


class EquipmentSnServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询SN列表"""

        equipment_sn_qs = EquipmentSn.search(**search_info)

        equipment_sn_qs.order_by("-create_time")
        return Splitor(current_page, equipment_qs)

    @classmethod
    def get_equipment_sn_status(cls, status):
        if status == "red":
            return SnStatusType.RED
        elif status == "yellow":
            return SnStatusType.YELLOW
        elif status == "green":
            return SnStatusType.GREEN
        elif status == "tgreen":
            return SnStatusType.TGREEB

    @classmethod
    def hung_sn_fororder(cls, order_list):
        order_mapping = {}
        for order in order_list:
            order_mapping[order.id] = order
            order.sn_list = []

        equipment_sn_qs = EquipmentSn.search(order_id__in = order_mapping.keys())
        for equipment_sn in equipment_sn_qs:
            if equipment_sn.order_id in order_mapping:
                order_mapping[equipment_sn.order_id].sn_list.append(equipment_sn)

        return order_list

    @classmethod
    def get_by_code(cls, code):
        equipment_sn = None
        equipment_sn_qs = EquipmentSn.search(code = code)
        if equipment_sn_qs.count() > 0:
            equipment_sn = equipment_sn_qs[0]
        return equipment_sn

class EquipmentRegisterServer(object):

    @classmethod
    def get(cls, id):
        """查询设备注册信息"""
        return EquipmentRegisterHelper.get(id)

    @classmethod
    def update(cls, equipment_register, **attrs):
        """修改设备注册信息"""
        return EquipmentRegisterHelper.update(equipment_register, **attrs)

    @classmethod
    def get_register_byequipment(cls, equipment):
        """根据设备查询注册信息"""
        return EquipmentRegisterHelper.get_register_byequipment(equipment)

