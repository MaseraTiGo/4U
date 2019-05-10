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

from model.models import EquipmentIn
from tuoen.sys.core.exception.business_error import BusinessError

class EquipmentInServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询設備入庫列表"""
        equipment_qs = EquipmentIn.search(**search_info)
        equipment_qs = equipment_qs.order_by("-create_time")

        return Splitor(current_page, equipment_qs)

    @classmethod
    def update(cls, id, **update_info):
        """"編輯設備入庫信息"""
        try:
            ei = EquipmentIn.search(id=id).update(**update_info)
            return ei
        except Exception as e:
            raise BusinessError("編輯提交失敗")
