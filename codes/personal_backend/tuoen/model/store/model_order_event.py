# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.store.model_order import Order
from model.store.model_event_base import EventBase

class IsCount(object):
    COUNTIN = 'countin'
    COUNTOUT = 'countout'
    CHOICES = ((COUNTIN, "计算"), (COUNTOUT, "不计算"))

class StaffOrderEvent(EventBase):
    """员工下单事件表"""
    order = ForeignKey(Order, on_delete=CASCADE)
    is_count = CharField(verbose_name = "是否计算", max_length = 24, choices = IsCount.CHOICES, default = IsCount.COUNTIN)
    describe = TextField(verbose_name = "描述", null = True, default = "")

    @classmethod
    def search(cls, **attrs):
        event_qs = cls.query().filter(**attrs)
        return event_qs
