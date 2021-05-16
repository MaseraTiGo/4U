# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class ImportStatus(object):
    INIT = "init"
    EXCUTTING = "excutting"
    FINISH = "finish"
    FAILED = "failed"

    CHOICES = ((INIT, "初始化"), (EXCUTTING, "执行中"), (FINISH, "已完成"), (FAILED, "失败"))


class BaseImport(BaseModel):
    status = CharField(verbose_name="执行状态", max_length=24, choices=ImportStatus.CHOICES, default=ImportStatus.INIT)

    error_text = TextField(verbose_name="转化失败描述", default="")

    class Meta:
        abstract = True

    @classmethod
    def search(cls, **attrs):
        order_qs = cls.query().filter(**attrs)
        return order_qs
