# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *

from model import AGENT_PREFIX
from model.base import BaseModel


class MyManager(Manager):
    def get_queryset(self):
        super_qs = super().get_queryset()
        return super_qs.exclude(status=Company.ComStatus.DELETE)


class Company(BaseModel):
    """机构表"""

    class ComStatus(IntegerChoices):
        ABNORMAL = 0
        NORMAL = 1
        DELETE = 2

    name = CharField(verbose_name="机构名称", max_length=32, default='')
    unique_id = CharField(verbose_name='机构唯一标识符', max_length=32, default='')
    address = CharField(verbose_name="机构地址", max_length=50, default='')
    phone = CharField(verbose_name="机构电话", max_length=32, default='')
    login_url = CharField(verbose_name="登录地址", max_length=64, default='')
    status = IntegerField(verbose_name="机构状态", default=ComStatus.NORMAL, choices=ComStatus.choices)

    objects = MyManager()

    class Meta:
        db_table = AGENT_PREFIX + 'company'
