# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.store.model_merchant_equipment import MerchantEquipment


class MerchantEquipmentHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户设备关系表"""
        merchant_equipment = MerchantEquipment.create(**attrs)
        if merchant_equipment is None:
            raise BusinessError("商户设备关系建立失败")
        return merchant_equipment

    @classmethod
    def get_by_serialNo(cls, serial_no):
        """根据设备硬件序列号查询"""
        merchant_equipment = None
        merchant_equipment_qs = MerchantEquipment.query(serial_no = serial_no)
        if merchant_equipment_qs.count() > 0:
            merchant_equipment = merchant_equipment_qs[0]
        return merchant_equipment

    @classmethod
    def batch_generate(cls, merchant_equipment_list):
        """批量添加商户设备关系表"""
        merchant_equipments = []
        for item in merchant_equipment_list:
            if cls.get_by_serialNo(item["serial_no"]) is None:
                merchant_equipments.append(MerchantEquipment(merchant = item["merchant"], equipment_sn = item["equipment_sn"], \
                                                             serial_no = item["serial_no"], terminal_id = item["terminal_id"], \
                                                             binding_date = item["binding_date"]))
        MerchantEquipment.objects.bulk_create(merchant_equipments)
        return True
