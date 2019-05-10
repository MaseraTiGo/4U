# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from model.base import BaseModel
from model.store.model_user import User


class GenderType(object):
    MADAM = 2
    MAN = 1
    UNKNOWN = 0
    CHOICES = ((UNKNOWN, '未知'), (MAN, "男"), (MADAM, "女"))


class Customer(BaseModel):
    user = OneToOneField(User)
    name = CharField(verbose_name="姓名", max_length=64, default="")
    gender = IntegerField(verbose_name="性别", choices=GenderType.CHOICES, default=GenderType.UNKNOWN)
    city = CharField(verbose_name="城市", max_length=128)
    address = CharField(verbose_name="详细地址", max_length=128)

    @classmethod
    def get_byuser(cls, user):
        try:
            return cls.objects.get(user=user)
        except:
            return None
