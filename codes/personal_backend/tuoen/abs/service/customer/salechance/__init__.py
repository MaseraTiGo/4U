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

from model.models import SaleChance


class SaleChanceHelper(object):

    @classmethod
    def generate(cls, **attr):
        """添加销售机会"""

        sale_chance = SaleChance.create(**attr)
        if sale_chance is None:
            raise BusinessError("添加失败")

    @classmethod
    def search(cls, current_page, **search_info):
        """查询销售机会列表"""
        sale_chance_qs = SaleChance.search(**search_info)
        today = datetime.date.today()
        sale_chance_qs = sale_chance_qs.filter(end_time__gte = today).order_by("end_time")
        return Splitor(current_page, sale_chance_qs)

    @classmethod
    def get(cls, sale_chance_id):
        """获取销售机会详情"""

        sale_chance = SaleChance.get_byid(sale_chance_id)
        if sale_chance is None:
            raise BusinessError("销售机会不存在")
        return sale_chance

    @classmethod
    def update(cls, sale_chance_id, **attrs):
        """编辑销售机会"""

        sale_chance = cls.get(sale_chance_id)

        sale_chance.update(**attrs)
        return True
