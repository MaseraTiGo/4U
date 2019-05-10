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

from model.models import EquipmentRegister


class EquipmentRegisterHelper(object):

    @classmethod
    def get(cls, id):
        """查询设备注册信息"""
        equipment_register = EquipmentRegister.get_byid(id)

        if equipment_register is None:
            raise BusinessError("设备注册信息不存在")

        return equipment_register

    @classmethod
    def update(cls, equipment_register, **attrs):
        """修改设备注册信息"""
        equipment_register.update(**attrs)
        return equipment_register

    @classmethod
    def get_register_byequipment(cls, equipment):
        """根据设备查询注册信息"""
        equipment_register_qs = EquipmentRegister.query(equipment = equipment)
        if equipment_register_qs.count() > 0:
            return equipment_register_qs[0]
        return None
