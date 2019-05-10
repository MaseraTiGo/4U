# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.store.model_customer import Customer
from model.store.model_event_base import EventBase


class TrackEvent(EventBase):
    """跟踪事件表"""
    customer = ForeignKey(Customer, on_delete=CASCADE)
    describe = TextField(verbose_name = "描述")

    @classmethod
    def search(cls, **attrs):
        track_event_qs = cls.query().filter(**attrs)
        return track_event_qs
