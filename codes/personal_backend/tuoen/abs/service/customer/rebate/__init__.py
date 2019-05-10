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

from model.models import EquipmentRebate


class RebateServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询返利列表"""
        rebate_qs = EquipmentRebate.search(**search_info)
        rebate_qs = rebate_qs.order_by("-id")

        return Splitor(current_page, rebate_qs)
