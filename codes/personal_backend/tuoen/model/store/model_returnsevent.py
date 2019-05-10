# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_department import Department
from model.store.model_orderreturns import OrderReturns
from model.store.model_department import Department
from model.store.model_event_base import EventBase

class StaffReturnsEvent(EventBase):
    '''退货事件'''
    server = ForeignKey(Staff, related_name = 'server', null = True, on_delete=CASCADE)
    order_returns = ForeignKey(OrderReturns, on_delete=CASCADE)
    describe = TextField(verbose_name = "描述", null = True, default = "")

    @classmethod
    def search(cls, **attrs):
        event_qs = cls.query().filter(**attrs)
        return event_qs
