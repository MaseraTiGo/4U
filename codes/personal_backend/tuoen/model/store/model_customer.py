# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import BaseUser
from model.store.model_mobilephone import MobileDevices


class Customer(BaseUser):
    """客户表"""
    wechat = CharField(verbose_name = "微信号", max_length = 128, default = "", null = True)
    nick = CharField(verbose_name = "昵称", max_length = 128, default = "", null = True)
    mobiledevices = ForeignKey(MobileDevices, null = True, on_delete=CASCADE)

    @classmethod
    def search(cls, **attrs):
        customer_qs = cls.query().filter(**attrs)
        return customer_qs
