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

from model.store.model_equipment_register import EquipmentRegister


class CustomerRegisterHelper(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询客戶註冊列表"""
        device_code = ""
        if 'code' in search_info:
            code = search_info.pop('code')
            search_info.update({'code': code})
        if 'status' in search_info:
            status = search_info.pop('status')
            search_info.update({'status': status})
        if 'device_code' in search_info:
            device_code = search_info.pop('device_code')
        if 'bind_time_start' in search_info:
            bind_time_start = search_info.pop('bind_time_start')
            search_info.update({'bind_time__gte': bind_time_start})
        if 'bind_time_end' in search_info:
            bind_time_end = search_info.pop('bind_time_end')
            search_info.update({'bind_time__lte': datetime.datetime(bind_time_end.year, bind_time_end.month, bind_time_end.day, 23, 59, 59)})

        customer_register_qs = EquipmentRegister.query().filter(**search_info)

        if device_code:
            customer_register_qs = customer_register_qs.filter(Q(device_code = device_code) \
                | Q(equipment_sn__code = device_code))

        customer_register_qs = customer_register_qs.order_by("-create_time")

        return Splitor(current_page, customer_register_qs)

    @classmethod
    def get(cls, sale_chance_id):
        """获取销售机会详情"""

        sale_chance = SaleChance.get_byid(sale_chance_id)
        if sale_chance is None:
            raise BusinessError("销售机会不存在")
        return sale_chance

    @classmethod
    def search_all(cls, **search_info):
        """查询所有客戶注册列表"""
        return EquipmentRegister.search(**search_info)


