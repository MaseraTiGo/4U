# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class Department(BaseModel):
    name = CharField(verbose_name = "部门名称", max_length = 64, default = "")
    parent_id = IntegerField(verbose_name = "对应上级部门id", default = 0)
    describe = TextField(verbose_name = "描述", default = "")
    status = BooleanField(verbose_name = "状态", default = True)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        department_qs = cls.query().filter(**attrs)
        return department_qs
