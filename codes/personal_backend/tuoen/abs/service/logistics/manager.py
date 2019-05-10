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

from model.models import Logistics, LogisticsItem


class LogisticsServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询物流列表"""

        logistics_qs = Logistics.query(**search_info)

        return logistics_qs

    @classmethod
    def hung_item_fororder(cls, order):
        """订单挂载物流"""

        logistics_qs = cls.search(order = order)
        for logistics in logistics_qs:
            LogisticsItemServer.hung_item_forlogistics(logistics)

        order.logistics = logistics_qs

        return order

    @classmethod
    def hung_logistics_fororder(cls, order_list):
        order_mapping = {}
        for order in order_list:
            order_mapping[order.id] = order
            order.logistics_list = []

        logistics_qs = cls.search(order_id__in = order_mapping.keys())
        for logistics in logistics_qs:
            if logistics.order_id in order_mapping:
                order_mapping[logistics.order_id].logistics_list.append(logistics)

        return order_list

class LogisticsItemServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询物流详情列表"""

        logistics_item_qs = LogisticsItem.query(**search_info)

        return logistics_item_qs

    @classmethod
    def hung_item_forlogistics(cls, logistics):
        """物流详情挂在物流"""

        logistics.items = cls.search(logistics = logistics)

        return logistics
