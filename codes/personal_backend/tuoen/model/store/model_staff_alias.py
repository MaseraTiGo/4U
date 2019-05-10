# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel

from model.store.model_user import Staff


class StaffAlias(BaseModel):
    """员工别名表"""
    staff = ForeignKey(Staff, null = True, on_delete=CASCADE)
    alias = CharField(verbose_name = "别名", max_length = 64, default = "")
    remark = TextField(verbose_name = "备注")
    
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
    
    @classmethod
    def search(cls, **attrs):
        staff_alias_qs = cls.query().filter(**attrs)
        return staff_alias_qs
