# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff


class JournalTypes(object):
    LOGIN = "login"
    OTHER = "other"
    DELETE = "delete"
    IMPORTRESET = "status reset"
    LOOK = "look"
    SEARCH = "search"
    EDIT = "edit"
    UPDATE = "update"
    ADD = "add"
    RECOVER = "recover"
    IMPORTDATA = "import"
    STARTUP = "startup"
    ALLOT = "allot"
    CHOICES = ((LOGIN, '登录'), (OTHER, "其它"), (IMPORTRESET, "导入数据状态重置"), (DELETE, "删除"), (LOOK, "查詢"), \
               (EDIT, "編輯"), (SEARCH, "搜索"), (UPDATE, "更新"), (ADD, "新增"), (IMPORTDATA, "数据导入"), \
               (RECOVER, "恢复"), (STARTUP, "启动"), (ALLOT, "分配")
               )


class OperationTypes(object):
    STAFF = "staff"
    USER = "user"
    SYSTEM = "system"
    AFTER_USER = 'after_user'
    CHOICES = ((STAFF, '员工'), (USER, "用户"), (SYSTEM, "系统"), (AFTER_USER, '售后用户'))


class Journal(BaseModel):
    """日志表"""
    active_uid = IntegerField(verbose_name="主动方uid", default=0)
    active_name = CharField(verbose_name="主动方姓名", max_length=8)
    active_type = CharField(verbose_name="主动方类型", max_length=12, choices=OperationTypes.CHOICES,
                            default=OperationTypes.SYSTEM)
    passive_uid = IntegerField(verbose_name="被动方uid", default=0)
    passive_name = CharField(verbose_name="被动方姓名", max_length=8)
    passive_type = CharField(verbose_name="被动方类型", max_length=12, choices=OperationTypes.CHOICES,
                             default=OperationTypes.SYSTEM)
    journal_type = CharField(verbose_name="日志类型", max_length=16, choices=JournalTypes.CHOICES,
                             default=JournalTypes.OTHER)
    record_detail = CharField(verbose_name="详情", max_length=250)
    remark = CharField(verbose_name="备注", max_length=64)

    class Meta:
        # db_table = 'journal'
        abstract = True

    @classmethod
    def search(cls, **attrs):
        journal_qs = cls.query().filter(**attrs)
        return journal_qs
