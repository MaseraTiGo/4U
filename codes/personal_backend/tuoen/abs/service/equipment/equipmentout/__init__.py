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

from model.models import EquipmentOut
from tuoen.sys.core.exception.business_error import BusinessError

class EquipmentOutServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询設備出庫列表"""
        equiment_qs = EquipmentOut.search(**search_info)
        equiment_qs = equiment_qs.order_by("-create_time")

        return Splitor(current_page, equiment_qs)

    @classmethod
    def update(cls, id, **update_info):
        """"編輯設備出庫信息"""
        try:
            eo = EquipmentOut.search(id=id).update(**update_info)
            return eo
        except Exception as e:
            raise BusinessError("編輯提交失敗")
